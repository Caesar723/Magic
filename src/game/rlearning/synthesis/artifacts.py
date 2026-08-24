"""Read/write helpers for synthesis artifacts.

The artifact directory is the source of truth.  The viewer consumes only these
JSON files, so it never has to load a checkpoint or run a model.
"""

from __future__ import annotations

import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np


SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: Any) -> None:
    temporary_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    os.replace(temporary_path, path)


def _replace_module(destination: Path, module_name: str, temporary_module: Path) -> Path:
    """Atomically publish a complete module directory."""
    module_path = destination / module_name
    backup_path: Path | None = None
    if module_path.exists():
        backup_path = destination / f".{module_name}-{uuid.uuid4().hex}.previous"
        os.replace(module_path, backup_path)

    try:
        os.replace(temporary_module, module_path)
    except Exception:
        if backup_path is not None and backup_path.exists():
            os.replace(backup_path, module_path)
        raise
    finally:
        if temporary_module.exists():
            shutil.rmtree(temporary_module, ignore_errors=True)

    if backup_path is not None:
        shutil.rmtree(backup_path, ignore_errors=True)
    return module_path


def _update_manifest(
    destination: Path,
    *,
    step: int,
    module_name: str,
    module_metadata: dict[str, Any],
    generated_at: str,
    checkpoint: str | None = None,
) -> None:
    manifest_path = destination / "manifest.json"
    manifest = _read_json(manifest_path, {})
    manifest.update(
        {
            "schema_version": SCHEMA_VERSION,
            "step": int(step),
            "generated_at": generated_at,
        }
    )
    if checkpoint is not None:
        manifest["checkpoint"] = checkpoint
    modules = manifest.setdefault("modules", {})
    if not isinstance(modules, dict):
        modules = {}
        manifest["modules"] = modules
    modules[module_name] = module_metadata
    _write_json(manifest_path, manifest)


def write_reconstruction_artifact(
    step_dir: str | Path,
    *,
    step: int,
    samples: Iterable[dict[str, Any]],
    checkpoint: str | None = None,
) -> Path:
    """Write one complete reconstruction module and register it in manifest.

    The module is built in a sibling temporary directory and only becomes
    visible after the complete directory has been moved into place.  This lets
    a running viewer safely scan while training is writing a new step.
    """
    destination = Path(step_dir)
    destination.mkdir(parents=True, exist_ok=True)

    temporary_module = destination / f".reconstruction-{uuid.uuid4().hex}.tmp"
    samples_dir = temporary_module / "samples"
    samples_dir.mkdir(parents=True)

    index_samples: list[dict[str, Any]] = []
    for sample_number, sample in enumerate(samples):
        sample_payload = dict(sample)
        sample_id = str(sample_payload.get("sample_id", f"{sample_number:03d}"))
        sample_payload["sample_id"] = sample_id

        sample_path = samples_dir / f"{sample_id}.json"
        _write_json(sample_path, sample_payload)

        summary = sample_payload.get("summary", {})
        index_samples.append(
            {
                "sample_id": sample_id,
                "source_index": sample_payload.get("source_index"),
                "path": f"samples/{sample_id}.json",
                "summary": summary,
            }
        )

    generated_at = utc_now()
    index_payload = {
        "schema_version": SCHEMA_VERSION,
        "step": int(step),
        "generated_at": generated_at,
        "samples": index_samples,
    }
    _write_json(temporary_module / "index.json", index_payload)

    module_path = _replace_module(destination, "reconstruction", temporary_module)
    _update_manifest(
        destination,
        step=step,
        module_name="reconstruction",
        module_metadata={
            "status": "complete",
            "sample_count": len(index_samples),
            "index": "reconstruction/index.json",
            "generated_at": generated_at,
        },
        generated_at=generated_at,
        checkpoint=checkpoint,
    )
    return module_path


def write_transition_space_artifact(
    step_dir: str | Path,
    *,
    step: int,
    vectors: dict[str, np.ndarray],
    records: Iterable[dict[str, Any]],
    coordinates: np.ndarray,
    projection: dict[str, Any],
) -> Path:
    """Write raw latent vectors and browser-ready projected points."""
    destination = Path(step_dir)
    destination.mkdir(parents=True, exist_ok=True)

    vector_arrays = {
        name: np.asarray(values, dtype=np.float32)
        for name, values in vectors.items()
    }
    if "mean_q" not in vector_arrays:
        raise ValueError("Transition-space vectors must include mean_q")

    point_records = [dict(record) for record in records]
    coordinates = np.asarray(coordinates, dtype=np.float32)
    if coordinates.shape != (len(point_records), 2):
        raise ValueError(
            f"Expected projection shape {(len(point_records), 2)}, got {coordinates.shape}"
        )
    for name, values in vector_arrays.items():
        if values.shape[0] != len(point_records):
            raise ValueError(
                f"Vector array {name} has {values.shape[0]} rows for {len(point_records)} records"
            )

    for point, coordinate in zip(point_records, coordinates):
        point["x"] = round(float(coordinate[0]), 7)
        point["y"] = round(float(coordinate[1]), 7)

    temporary_module = destination / f".transition_space-{uuid.uuid4().hex}.tmp"
    temporary_module.mkdir(parents=True)
    np.savez_compressed(temporary_module / "vectors.npz", **vector_arrays)

    generated_at = utc_now()
    _write_json(
        temporary_module / "points.json",
        {
            "schema_version": SCHEMA_VERSION,
            "step": int(step),
            "projection": projection,
            "points": point_records,
        },
    )
    highlight_count = sum(bool(point.get("is_highlighted")) for point in point_records)
    _write_json(
        temporary_module / "index.json",
        {
            "schema_version": SCHEMA_VERSION,
            "step": int(step),
            "generated_at": generated_at,
            "point_count": len(point_records),
            "highlight_count": highlight_count,
            "vector_dimensions": int(vector_arrays["mean_q"].shape[1]),
            "projection": projection,
            "points": "points.json",
            "vectors": "vectors.npz",
        },
    )

    module_path = _replace_module(destination, "transition_space", temporary_module)
    _update_manifest(
        destination,
        step=step,
        module_name="transition_space",
        module_metadata={
            "status": "complete",
            "point_count": len(point_records),
            "highlight_count": highlight_count,
            "index": "transition_space/index.json",
            "generated_at": generated_at,
        },
        generated_at=generated_at,
    )
    return module_path


def write_text_embedding_space_artifact(
    step_dir: str | Path,
    *,
    step: int,
    embeddings: np.ndarray,
    records: Iterable[dict[str, Any]],
    coordinates: np.ndarray,
    projection: dict[str, Any],
) -> Path:
    """Write text embeddings and their browser-ready two-dimensional view."""
    destination = Path(step_dir)
    destination.mkdir(parents=True, exist_ok=True)

    embedding_array = np.asarray(embeddings, dtype=np.float32)
    point_records = [dict(record) for record in records]
    coordinates = np.asarray(coordinates, dtype=np.float32)
    if embedding_array.ndim != 2:
        raise ValueError(f"Expected a 2D embedding matrix, got shape {embedding_array.shape}")
    if coordinates.shape != (len(point_records), 2):
        raise ValueError(
            f"Expected projection shape {(len(point_records), 2)}, got {coordinates.shape}"
        )
    if embedding_array.shape[0] != len(point_records):
        raise ValueError(
            f"Embedding matrix has {embedding_array.shape[0]} rows for "
            f"{len(point_records)} records"
        )

    for point, coordinate in zip(point_records, coordinates):
        point["x"] = round(float(coordinate[0]), 7)
        point["y"] = round(float(coordinate[1]), 7)

    temporary_module = destination / f".text_embedding_space-{uuid.uuid4().hex}.tmp"
    temporary_module.mkdir(parents=True)
    np.savez_compressed(temporary_module / "embeddings.npz", embeddings=embedding_array)

    generated_at = utc_now()
    _write_json(
        temporary_module / "points.json",
        {
            "schema_version": SCHEMA_VERSION,
            "step": int(step),
            "projection": projection,
            "points": point_records,
        },
    )
    query_count = sum(point.get("kind") == "query" for point in point_records)
    card_count = sum(point.get("kind") == "card" for point in point_records)
    _write_json(
        temporary_module / "index.json",
        {
            "schema_version": SCHEMA_VERSION,
            "step": int(step),
            "generated_at": generated_at,
            "point_count": len(point_records),
            "query_count": query_count,
            "card_count": card_count,
            "vector_dimensions": int(embedding_array.shape[1]),
            "projection": projection,
            "points": "points.json",
            "embeddings": "embeddings.npz",
        },
    )

    module_path = _replace_module(destination, "text_embedding_space", temporary_module)
    _update_manifest(
        destination,
        step=step,
        module_name="text_embedding_space",
        module_metadata={
            "status": "complete",
            "point_count": len(point_records),
            "query_count": query_count,
            "card_count": card_count,
            "index": "text_embedding_space/index.json",
            "generated_at": generated_at,
        },
        generated_at=generated_at,
    )
    return module_path
