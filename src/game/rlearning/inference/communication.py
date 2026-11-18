from multiprocessing import Queue

from game.rlearning.utils.model import get_class_by_name


class InferenceCommunication:
    def __init__(self,num_worker,input_packing=None):
        self.request_queue=Queue()
        self.control_queue=Queue()
        self.response_queues=[
            Queue() for _ in range(num_worker)
        ]

        settings=input_packing or {}
        self.state_packer=None

        if settings.get("enabled",False):
            self.state_packer=get_class_by_name(
                settings["class_name"]
            )()

    def pack_state(self,state,config_path):
        if self.state_packer is None:
            return state
        return self.state_packer(state,config_path)