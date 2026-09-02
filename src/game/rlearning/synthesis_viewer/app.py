"""FastAPI application for browsing synthesis artifacts."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .repository import ArtifactNotFoundError, ArtifactRepository


PACKAGE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))


def _reconstruction_prediction_options(sample: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize new dual-encoder artifacts and the legacy single view."""
    predictions = sample.get("predictions")
    if isinstance(predictions, dict):
        options = []
        for key in ("prior", "posterior"):
            prediction = predictions.get(key)
            if not isinstance(prediction, dict):
                continue
            options.append(
                {
                    "key": key,
                    "label": str(
                        prediction.get(
                            "label",
                            "Prior · inference"
                            if key == "prior"
                            else "Posterior · reconstruction",
                        )
                    ),
                    "prediction": prediction,
                }
            )
        if options:
            return options

    # Artifacts made before dual visualization used only Posterior mean_q.
    return [
        {
            "key": "posterior",
            "label": "Posterior · reconstruction",
            "prediction": {
                "encoder": "PosteriorEncoder",
                "label": "Posterior · reconstruction",
                "condition": "current state + card + action + true next state",
                "metrics": sample.get("metrics", {}),
                "entity_transitions": sample.get("entity_transitions"),
                "predicted_next_state": sample.get("predicted_next_state"),
            },
        }
    ]


def _transition_projection_options(index: dict[str, Any]) -> list[dict[str, str]]:
    available = index.get("latent_views")
    if not isinstance(available, list):
        available = ["posterior"]
    labels = {
        "prior": "Prior · inference",
        "posterior": "Posterior · reconstruction",
    }
    options = [
        {"key": key, "label": labels.get(key, str(key).replace("_", " ").title())}
        for key in ("prior", "posterior")
        if key in available
    ]
    return options or [{"key": "posterior", "label": labels["posterior"]}]


def _render(request: Request, template_name: str, **context):
    repository: ArtifactRepository = request.app.state.repository
    context.setdefault("experiments", repository.list_experiments())
    return templates.TemplateResponse(request=request, name=template_name, context=context)


def _not_found(error: ArtifactNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


def _step_navigation(
    request: Request,
    experiment_id: str,
    current_step: int,
    endpoint: str,
    module_name: str | None = None,
) -> dict[str, Any]:
    """Build links for the browseable snapshots of a single viewer.

    A snapshot can exist before every module finishes writing.  Filtering by the
    requested module means changing steps in a visualization never sends a user
    to a 404 page for a missing artifact.
    """
    repository: ArtifactRepository = request.app.state.repository
    available_steps: list[dict[str, Any]] = []
    for step_info in repository.list_steps(experiment_id):
        if module_name is not None:
            module = step_info["manifest"].get("modules", {}).get(module_name)
            if not isinstance(module, dict) or module.get("status") != "complete":
                continue

        step = step_info["step"]
        available_steps.append(
            {
                "step": step,
                "url": str(
                    request.url_for(
                        endpoint,
                        experiment_id=experiment_id,
                        step=step,
                    )
                ),
            }
        )

    available_steps.sort(key=lambda item: item["step"])
    current_index = next(
        index
        for index, item in enumerate(available_steps)
        if item["step"] == current_step
    )
    return {
        "available_steps": available_steps,
        "current": available_steps[current_index],
        "older": (
            available_steps[current_index - 1] if current_index > 0 else None
        ),
        "newer": (
            available_steps[current_index + 1]
            if current_index + 1 < len(available_steps)
            else None
        ),
    }


def create_app(logdir: str | Path) -> FastAPI:
    app = FastAPI(title="Synthesis Viewer", docs_url=None, redoc_url=None)
    app.state.repository = ArtifactRepository(logdir)
    app.mount("/static", StaticFiles(directory=str(PACKAGE_DIR / "static")), name="static")

    @app.get("/", name="home")
    async def home(request: Request):
        experiments = request.app.state.repository.list_experiments()
        if len(experiments) == 1:
            return RedirectResponse(
                request.url_for("experiment_page", experiment_id=experiments[0].id),
                status_code=303,
            )
        return _render(request, "experiments.html", title="Synthesis Viewer")

    @app.get("/experiments/{experiment_id}", name="experiment_page")
    async def experiment_page(request: Request, experiment_id: str):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            steps = repository.list_steps(experiment_id)
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error
        return _render(
            request,
            "experiment.html",
            title=f"{experiment.name} · Synthesis",
            experiment=experiment,
            current_experiment_id=experiment.id,
            steps=steps,
        )

    @app.get("/experiments/{experiment_id}/{step}", name="step_page")
    async def step_page(request: Request, experiment_id: str, step: int):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            step_info = repository.get_step(experiment_id, step)
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error
        return _render(
            request,
            "step.html",
            title=f"{experiment.name} · step {step}",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step_info=step_info,
            step_navigation=_step_navigation(
                request,
                experiment.id,
                step_info["step"],
                "step_page",
            ),
        )

    @app.get(
        "/experiments/{experiment_id}/{step}/reconstruction",
        name="reconstruction_page",
    )
    async def reconstruction_page(request: Request, experiment_id: str, step: int):
        repository: ArtifactRepository = request.app.state.repository
        try:
            index = repository.reconstruction_index(experiment_id, step)
            first_sample = next(iter(index.get("samples", [])), None)
            if not isinstance(first_sample, dict):
                raise ArtifactNotFoundError("This reconstruction has no samples")
            sample_id = str(first_sample["sample_id"])
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error
        return RedirectResponse(
            request.url_for(
                "reconstruction_sample_page",
                experiment_id=experiment_id,
                step=step,
                sample_id=sample_id,
            ),
            status_code=303,
        )

    @app.get(
        "/experiments/{experiment_id}/{step}/reconstruction/{sample_id}",
        name="reconstruction_sample_page",
    )
    async def reconstruction_sample_page(
        request: Request,
        experiment_id: str,
        step: int,
        sample_id: str,
        encoder: str = "prior",
    ):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            index, sample = repository.reconstruction_sample(experiment_id, step, sample_id)
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error
        prediction_options = _reconstruction_prediction_options(sample)
        selected_option = next(
            (option for option in prediction_options if option["key"] == encoder),
            prediction_options[0],
        )
        selected_encoder = selected_option["key"]
        sample_urls = {
            str(item["sample_id"]): (
                f"{request.url_for('reconstruction_sample_page', experiment_id=experiment_id, step=step, sample_id=item['sample_id'])}"
                f"?encoder={selected_encoder}"
            )
            for item in index.get("samples", [])
            if isinstance(item, dict) and item.get("sample_id") is not None
        }
        prediction_urls = {
            option["key"]: (
                f"{request.url_for('reconstruction_sample_page', experiment_id=experiment_id, step=step, sample_id=sample_id)}"
                f"?encoder={option['key']}"
            )
            for option in prediction_options
        }
        return _render(
            request,
            "reconstruction.html",
            title=f"{experiment.name} · {step} · reconstruction",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step=step,
            index=index,
            sample=sample,
            prediction=selected_option["prediction"],
            prediction_options=prediction_options,
            selected_encoder=selected_encoder,
            sample_urls=sample_urls,
            prediction_urls=prediction_urls,
            step_navigation=_step_navigation(
                request,
                experiment.id,
                step,
                "reconstruction_page",
                module_name="reconstruction",
            ),
        )

    @app.get(
        "/experiments/{experiment_id}/{step}/transition-space",
        name="transition_space_page",
    )
    async def transition_space_page(
        request: Request,
        experiment_id: str,
        step: int,
    ):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            index, points_payload = repository.transition_space(
                experiment_id,
                step,
            )
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error

        points = []
        for source_point in points_payload.get("points", []):
            point = dict(source_point)
            sample_id = point.get("reconstruction_sample_id")
            if sample_id is not None:
                reconstruction_url = str(
                    request.url_for(
                        "reconstruction_sample_page",
                        experiment_id=experiment_id,
                        step=step,
                        sample_id=sample_id,
                    )
                )
                point["reconstruction_urls"] = {
                    "prior": reconstruction_url + "?encoder=prior",
                    "posterior": reconstruction_url + "?encoder=posterior",
                }
                point["reconstruction_url"] = point["reconstruction_urls"]["prior"]
            points.append(point)

        return _render(
            request,
            "transition_space.html",
            title=f"{experiment.name} · {step} · transition space",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step=step,
            index=index,
            points=points,
            projection_options=_transition_projection_options(index),
            step_navigation=_step_navigation(
                request,
                experiment.id,
                step,
                "transition_space_page",
                module_name="transition_space",
            ),
        )

    @app.get(
        "/experiments/{experiment_id}/{step}/text-embedding-space",
        name="text_embedding_space_page",
    )
    async def text_embedding_space_page(
        request: Request,
        experiment_id: str,
        step: int,
    ):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            index, points_payload = repository.text_embedding_space(
                experiment_id,
                step,
            )
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error

        return _render(
            request,
            "text_embedding_space.html",
            title=f"{experiment.name} · {step} · text embeddings",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step=step,
            index=index,
            points=points_payload.get("points", []),
            step_navigation=_step_navigation(
                request,
                experiment.id,
                step,
                "text_embedding_space_page",
                module_name="text_embedding_space",
            ),
        )

    @app.get(
        "/experiments/{experiment_id}/{step}/card-fusion-space",
        name="card_fusion_space_page",
    )
    async def card_fusion_space_page(
        request: Request,
        experiment_id: str,
        step: int,
    ):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            index, points_payload = repository.card_fusion_space(
                experiment_id,
                step,
            )
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error

        return _render(
            request,
            "card_fusion_space.html",
            title=f"{experiment.name} · {step} · CardFusion",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step=step,
            index=index,
            points=points_payload.get("points", []),
            step_navigation=_step_navigation(
                request,
                experiment.id,
                step,
                "card_fusion_space_page",
                module_name="card_fusion_space",
            ),
        )

    return app


def app_from_env() -> FastAPI:
    """Uvicorn factory used by ``--reload``."""
    logdir = os.environ.get("SYNTHESIS_VIEWER_LOGDIR")
    if not logdir:
        raise RuntimeError("SYNTHESIS_VIEWER_LOGDIR is required when using the app factory")
    return create_app(logdir)
