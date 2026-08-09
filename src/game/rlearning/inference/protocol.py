from dataclasses import dataclass
from typing import Any, Optional, Union


RestoreStep = Union[int, str]


@dataclass
class InferenceRequest:
    worker_id: int
    request_id: int
    policy_id: str
    config_path: str
    restore_step: RestoreStep
    state: dict[str, Any]


@dataclass
class InferenceResponse:
    request_id: int
    action: int
    policy_version: RestoreStep
    error: Optional[str] = None


@dataclass
class PolicyUpdate:
    policy_id: str
    config_path: str
    restore_step: RestoreStep
