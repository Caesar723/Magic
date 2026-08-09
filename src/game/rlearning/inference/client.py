from typing import Optional

from .protocol import InferenceRequest, RestoreStep


class InferenceClient:
    """CPU-only policy client used inside one rollout worker."""

    def __init__(self, communication, worker_id: int, policy_id: str, config_path: str,
                 restore_step: RestoreStep = 0):
        self.communication = communication
        self.worker_id = worker_id
        self.policy_id = policy_id
        self.config_path = config_path
        self.restore_step = restore_step
        self._request_id = 0

    def configure(self, config_path: Optional[str] = None,
                  restore_step: Optional[RestoreStep] = None):
        if config_path is not None:
            self.config_path = config_path
        if restore_step is not None:
            self.restore_step = restore_step

    def choose_action(self, state: dict) -> dict:
        request_id = self._request_id
        self._request_id += 1
        self.communication.request_queue.put(InferenceRequest(
            worker_id=self.worker_id,
            request_id=request_id,
            policy_id=self.policy_id,
            config_path=self.config_path,
            restore_step=self.restore_step,
            state=state,
        ))
        while True:
            response = self.communication.response_queues[self.worker_id].get()
            if response.request_id != request_id:
                raise RuntimeError(
                    f"worker {self.worker_id} received an out-of-order inference response"
                )
            if response.error:
                raise RuntimeError(f"inference failed for {self.policy_id}: {response.error}")
            return {"action": response.action, "policy_version": response.policy_version}
