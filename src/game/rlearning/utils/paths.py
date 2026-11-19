from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv


class ProjectPaths:
    """Machine-specific storage paths, independent of the working directory."""

    def __init__(self, project_root=None):
        self.project_root = Path(project_root or Path(__file__).resolve().parents[4]).expanduser().resolve()
        load_dotenv(self.project_root / ".env", override=False)

        self.checkpoints = self._root("MAGIC_CHECKPOINT_ROOT", "/mnt/data/trainData/checkpoints")
        self.models = self._root("MAGIC_MODEL_ROOT", self.project_root / "models")
        self.cache = self._root("MAGIC_CACHE_ROOT", self.project_root / "cache")

    @classmethod
    @lru_cache(maxsize=1)
    def get(cls):
        return cls()

    def _root(self, name, default):
        value = os.environ.get(name, str(default))
        if not value.strip():
            raise ValueError(f"{name} must not be empty")

        path = Path(value).expanduser()
        return (self.project_root / path).resolve()

    @staticmethod
    def _relative_to(path, roots):
        for root in roots:
            try:
                return path.relative_to(Path(root).expanduser().resolve())
            except ValueError:
                continue
        return None

    def checkpoint_path(self, value, root=None):
        path = Path(value).expanduser()

        if path.is_absolute():
            path = path.resolve()
            relative = self._relative_to(path, (
                "/mnt/data/trainData/checkpoints",
                "/mnt/g/dataset/checkpoints",
            ))
            return (self.checkpoints / relative).resolve() if relative is not None else path

        if path.parts and path.parts[0] == "checkpoints":
            return (self.checkpoints / path.relative_to("checkpoints")).resolve()

        if path.parts and path.parts[0] == "logs":
            return (self.checkpoints / path).resolve()

        base = Path(root).expanduser() if root is not None else self.checkpoints
        return (base / path).resolve()

    def model_path(self, value):
        if not value:
            return None

        path = Path(value).expanduser()

        if path.is_absolute():
            path = path.resolve()
            checkpoint = self.checkpoint_path(path)
            if checkpoint != path:
                return checkpoint

            relative = self._relative_to(path, (
                self.project_root / "models",
                "/home/a123456/Desktop/Magic/models",
            ))
            return (self.models / relative).resolve() if relative is not None else path

        if path.parts and path.parts[0] == "models":
            path = path.relative_to("models")

        return (self.models / path).resolve()

    def cache_path(self, value=None):
        if not value:
            return (self.cache / "huggingface").resolve()

        path = Path(value).expanduser()

        if path.is_absolute():
            path = path.resolve()
            relative = self._relative_to(path, (
                self.project_root / "models",
                "/home/a123456/Desktop/Magic/models",
            ))
            return (self.cache / "huggingface" / relative).resolve() if relative is not None else path

        if path.parts and path.parts[0] == "models":
            return (self.cache / "huggingface" / path.relative_to("models")).resolve()

        if path.parts and path.parts[0] == "cache":
            path = path.relative_to("cache")

        return (self.cache / path).resolve()
