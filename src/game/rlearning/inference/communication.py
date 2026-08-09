from torch.multiprocessing import Queue


class InferenceCommunication:
    """IPC owned by the parent process and shared with rollout workers."""

    def __init__(self, num_worker: int):
        self.request_queue = Queue()
        self.control_queue = Queue()
        self.response_queues = [Queue() for _ in range(num_worker)]
