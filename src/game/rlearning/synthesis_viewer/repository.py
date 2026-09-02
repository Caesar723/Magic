"""Filesystem-backed, read-only access to synthesis artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ArtifactNotFoundError(LookupError):
    pass


@dataclass(frozen=True)
class Experiment:
    id: str
    name: str
    path: Path


class ArtifactRepository:
    def __init__(self, logdir: str | Path):
        self.logdir = Path(logdir).expanduser().resolve()
        if not self.logdir.is_dir():
            raise ValueError(f"Synthesis logdir does not exist or is not a directory: {self.logdir}")

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any] | None:
        try:
            with path.open("r", encoding="utf-8") as handle:
                value = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _is_experiment(path: Path) -> bool:
        return path.is_dir() and (path / "synthesis").is_dir()

    def list_experiments(self) -> list[Experiment]:
        if self._is_experiment(self.logdir):
            return [Experiment(id=self.logdir.name, name=self.logdir.name, path=self.logdir)]

        experiments = [
            Experiment(id=path.name, name=path.name, path=path)
            for path in self.logdir.iterdir()
            if self._is_experiment(path)
        ]
        return sorted(experiments, key=lambda experiment: experiment.name.casefold())

    def get_experiment(self, experiment_id: str) -> Experiment:
        for experiment in self.list_experiments():
            if experiment.id == experiment_id:
                return experiment
        raise ArtifactNotFoundError(f"Experiment not found: {experiment_id}")

    def list_steps(self, experiment_id: str) -> list[dict[str, Any]]:
        experiment = self.get_experiment(experiment_id)
        steps: list[dict[str, Any]] = []
        for path in (experiment.path / "synthesis").iterdir():
            if not path.is_dir() or not path.name.isdigit():
                continue
            manifest = self._read_json(path / "manifest.json")
            if manifest is None:
                continue
            steps.append(
                {
                    "step": int(path.name),
                    "manifest": manifest,
                    "path": path,
                }
            )
        return sorted(steps, key=lambda item: item["step"], reverse=True)

    def get_step(self, experiment_id: str, step: int) -> dict[str, Any]:
        for item in self.list_steps(experiment_id):
            if item["step"] == int(step):
                return item
        raise ArtifactNotFoundError(f"Synthesis step not found: {step}")

    @staticmethod
    def _artifact_path(step_path: Path, relative_path: str) -> Path:
        path = (step_path / relative_path).resolve()
        if not path.is_relative_to(step_path.resolve()):
            raise ArtifactNotFoundError("Invalid artifact path")
        return path

    def reconstruction_index(self, experiment_id: str, step: int) -> dict[str, Any]:
        step_info = self.get_step(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("reconstruction")
        if not isinstance(module, dict) or module.get("status") != "complete":
            raise ArtifactNotFoundError("Reconstruction is not available for this step")

        index_path = self._artifact_path(step_info["path"], str(module.get("index", "")))
        index = self._read_json(index_path)
        if index is None:
            raise ArtifactNotFoundError("Reconstruction index is unavailable")
        return index

    def reconstruction_sample(
        self, experiment_id: str, step: int, sample_id: str
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        step_info = self.get_step(experiment_id, step)
        index = self.reconstruction_index(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("reconstruction", {})
        index_path = self._artifact_path(step_info["path"], str(module.get("index", "")))
        sample_entry = next(
            (item for item in index.get("samples", []) if item.get("sample_id") == sample_id),
            None,
        )
        if not isinstance(sample_entry, dict):
            raise ArtifactNotFoundError(f"Reconstruction sample not found: {sample_id}")

        sample_path = self._artifact_path(index_path.parent, str(sample_entry.get("path", "")))
        sample = self._read_json(sample_path)
        if sample is None:
            raise ArtifactNotFoundError(f"Reconstruction sample is unavailable: {sample_id}")
        return index, sample

    def transition_space(self, experiment_id: str, step: int) -> tuple[dict, dict]:
        step_info = self.get_step(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("transition_space")
        if not isinstance(module, dict) or module.get("status") != "complete":
            raise ArtifactNotFoundError("Transition space is not available for this step")

        index_path = self._artifact_path(
            step_info["path"],
            str(module.get("index", "")),
        )
        index = self._read_json(index_path)
        if index is None:
            raise ArtifactNotFoundError("Transition-space index is unavailable")

        points_path = self._artifact_path(
            index_path.parent,
            str(index.get("points", "")),
        )
        points = self._read_json(points_path)
        if points is None:
            raise ArtifactNotFoundError("Transition-space points are unavailable")
        return index, points

    def transition_plan(self, experiment_id: str, step: int) -> tuple[dict, dict]:
        """Return the deterministic transition-plan projection for one snapshot."""
        step_info = self.get_step(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("transition_plan")
        if not isinstance(module, dict) or module.get("status") != "complete":
            raise ArtifactNotFoundError("Transition plan is not available for this step")
        index_path = self._artifact_path(step_info["path"], str(module.get("index", "")))
        index = self._read_json(index_path)
        if index is None:
            raise ArtifactNotFoundError("Transition-plan index is unavailable")
        points = self._read_json(self._artifact_path(index_path.parent, str(index.get("points", ""))))
        if points is None:
            raise ArtifactNotFoundError("Transition-plan points are unavailable")
        plan_points = points.get("points", [])
        try:
            _, transition_points = self.transition_space(experiment_id, step)
        except ArtifactNotFoundError:
            transition_points = {}
        records = transition_points.get("points", [])
        fields = ("source_index", "is_highlighted", "reconstruction_sample_id", "state_delta", "action", "card_used", "reconstruction_score", "reconstruction_scores")
        if len(records) == len(plan_points) and all(item.get("vector_index") == position for position, item in enumerate(records)):
            for point, record in zip(plan_points, records):
                for field in fields:
                    point.setdefault(field, record.get(field))
        return index, points

    def text_embedding_space(self, experiment_id: str, step: int) -> tuple[dict, dict]:
        step_info = self.get_step(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("text_embedding_space")
        if not isinstance(module, dict) or module.get("status") != "complete":
            raise ArtifactNotFoundError("Text embedding space is not available for this step")

        index_path = self._artifact_path(
            step_info["path"],
            str(module.get("index", "")),
        )
        index = self._read_json(index_path)
        if index is None:
            raise ArtifactNotFoundError("Text embedding-space index is unavailable")

        points_path = self._artifact_path(
            index_path.parent,
            str(index.get("points", "")),
        )
        points = self._read_json(points_path)
        if points is None:
            raise ArtifactNotFoundError("Text embedding-space points are unavailable")
        return index, points

    def card_fusion_space(self, experiment_id: str, step: int) -> tuple[dict, dict]:
        step_info = self.get_step(experiment_id, step)
        module = step_info["manifest"].get("modules", {}).get("card_fusion_space")
        if not isinstance(module, dict) or module.get("status") != "complete":
            raise ArtifactNotFoundError("CardFusion space is not available for this step")

        index_path = self._artifact_path(
            step_info["path"],
            str(module.get("index", "")),
        )
        index = self._read_json(index_path)
        if index is None:
            raise ArtifactNotFoundError("CardFusion-space index is unavailable")

        points_path = self._artifact_path(
            index_path.parent,
            str(index.get("points", "")),
        )
        points = self._read_json(points_path)
        if points is None:
            raise ArtifactNotFoundError("CardFusion-space points are unavailable")
        return index, points
