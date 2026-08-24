"""FastAPI application for browsing synthesis artifacts."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .repository import ArtifactNotFoundError, ArtifactRepository


PACKAGE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))


def _render(request: Request, template_name: str, **context):
    repository: ArtifactRepository = request.app.state.repository
    context.setdefault("experiments", repository.list_experiments())
    return templates.TemplateResponse(request=request, name=template_name, context=context)


def _not_found(error: ArtifactNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


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
        request: Request, experiment_id: str, step: int, sample_id: str
    ):
        repository: ArtifactRepository = request.app.state.repository
        try:
            experiment = repository.get_experiment(experiment_id)
            index, sample = repository.reconstruction_sample(experiment_id, step, sample_id)
        except ArtifactNotFoundError as error:
            raise _not_found(error) from error
        return _render(
            request,
            "reconstruction.html",
            title=f"{experiment.name} · {step} · reconstruction",
            experiment=experiment,
            current_experiment_id=experiment.id,
            step=step,
            index=index,
            sample=sample,
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
                point["reconstruction_url"] = str(
                    request.url_for(
                        "reconstruction_sample_page",
                        experiment_id=experiment_id,
                        step=step,
                        sample_id=sample_id,
                    )
                )
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
        )

    return app


def app_from_env() -> FastAPI:
    """Uvicorn factory used by ``--reload``."""
    logdir = os.environ.get("SYNTHESIS_VIEWER_LOGDIR")
    if not logdir:
        raise RuntimeError("SYNTHESIS_VIEWER_LOGDIR is required when using the app factory")
    return create_app(logdir)
