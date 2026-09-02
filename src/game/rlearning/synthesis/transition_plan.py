"""Compact artifacts for deterministic transition-plan vectors."""

import json
from pathlib import Path

import numpy as np

from game.rlearning.synthesis.projection import pca_project_2d


def write_transition_plan_artifact(step_dir, step, plan_tokens):
    """Save plan tokens, their mean summary and a deterministic two-dimensional view."""
    step_dir = Path(step_dir)
    destination = step_dir / "transition_plan"
    destination.mkdir(parents=True, exist_ok=True)
    tokens = np.asarray(plan_tokens, dtype=np.float32)
    summary = tokens.mean(axis=1)
    coordinates, projection = pca_project_2d(summary, source="plan_summary")
    np.savez_compressed(destination / "vectors.npz", plan_tokens=tokens, plan_summary=summary)
    points = [{"vector_index": index, "x": round(float(x), 7), "y": round(float(y), 7)} for index, (x, y) in enumerate(coordinates)]
    transition_path = step_dir / "transition_space" / "points.json"
    transition_data = json.loads(transition_path.read_text(encoding="utf-8")) if transition_path.is_file() else {}
    transition_points = transition_data.get("points", [])
    point_fields = ("source_index", "is_highlighted", "reconstruction_sample_id", "state_delta", "action", "card_used", "reconstruction_score", "reconstruction_scores")
    if len(transition_points) == len(points) and all(item.get("vector_index") == index for index, item in enumerate(transition_points)):
        for point, transition_point in zip(points, transition_points):
            point.update({field: transition_point[field] for field in point_fields if field in transition_point})
    index = {"schema_version": 1, "step": int(step), "point_count": len(points), "plan_token_count": int(tokens.shape[1]), "vector_dimensions": int(tokens.shape[2]), "projection": projection, "points": "points.json", "vectors": "vectors.npz"}
    (destination / "points.json").write_text(json.dumps({"schema_version": 1, "step": int(step), "projection": projection, "points": points}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (destination / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path = step_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    manifest.setdefault("modules", {})["transition_plan"] = {"status": "complete", "point_count": len(points), "index": "transition_plan/index.json"}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination
