import asyncio
import itertools
import pickle
import threading
from copy import deepcopy
from queue import Empty,Full
from torch.multiprocessing import get_context
from game.rlearning.inference.protocol import InferenceRequest
from game.rlearning.inference.server import inference_server_process


class PveInferenceCommunication:
    def __init__(self,context,max_pending:int):
        self.request_queue=context.Queue(maxsize=max_pending)
        self.control_queue=context.Queue()
        self.response_queues=[context.Queue()]

    def close(self):
        queues=[self.request_queue,self.control_queue,*self.response_queues]
        for queue in queues:
            queue.cancel_join_thread()
            queue.close()


class PveInference:
    def __init__(self,max_batch_size:int=32,max_wait_ms:int=10,timeout:float=120,max_pending:int=512):
        if max_batch_size<1 or max_wait_ms<0 or timeout<=0 or max_pending<1:
            raise ValueError("Invalid PVE inference configuration")

        self.config={"max_batch_size":max_batch_size,"max_wait_ms":max_wait_ms}
        self.timeout=timeout
        self.max_pending=max_pending
        self.context=get_context("spawn")
        self.communication=None
        self.process=None
        self.reader=None
        self.loop=None
        self.pending={}
        self.request_ids=itertools.count()
        self.running=False

    def start(self):
        if self.process is not None:
            raise RuntimeError("PVE inference is already started")

        self.loop=asyncio.get_running_loop()
        self.communication=PveInferenceCommunication(self.context,self.max_pending)
        self.process=self.context.Process(target=inference_server_process,args=(self.communication,self.config),name="pve-inference")

        try:
            self.process.start()
        except Exception:
            self.communication.close()
            self.communication=None
            self.process=None
            raise

        self.running=True
        self.reader=threading.Thread(target=self.read_responses,name="pve-inference-reader",daemon=True)
        self.reader.start()

    def post(self,callback,*args):
        if self.loop is None or self.loop.is_closed():
            return
        try:
            self.loop.call_soon_threadsafe(callback,*args)
        except RuntimeError:
            return

    def read_responses(self):
        response_queue=self.communication.response_queues[0]

        while self.running:
            try:
                response=response_queue.get(timeout=0.2)
            except Empty:
                if self.running and not self.process.is_alive():
                    self.post(self.fail_pending,f"PVE inference process exited with code {self.process.exitcode}")
                    return
            except (EOFError,OSError) as e:
                if self.running:
                    self.post(self.fail_pending,f"PVE inference connection failed: {e}")
                return
            else:
                self.post(self.deliver_response,response)

    def deliver_response(self,response):
        future=self.pending.pop(response.request_id,None)
        if future is None or future.done():
            return

        if response.error:
            future.set_exception(RuntimeError(response.error))
        else:
            result=dict(response.result)
            result["policy_version"]=response.policy_version
            future.set_result(result)

    def fail_pending(self,message:str):
        self.running=False
        futures=list(self.pending.values())
        self.pending.clear()
        for future in futures:
            if not future.done():
                future.set_exception(RuntimeError(message))

    async def choose_action(self,config_path:str,restore_step,state:dict):
        if not self.running or self.process is None or not self.process.is_alive():
            raise RuntimeError("PVE inference is not running")
        if asyncio.get_running_loop() is not self.loop:
            raise RuntimeError("PVE inference was called from a different event loop")
        if len(self.pending)>=self.max_pending:
            raise RuntimeError("Too many pending PVE inference requests")

        request_id=next(self.request_ids)
        request=InferenceRequest(
            worker_id=0,
            request_id=request_id,
            policy_id="pve",
            config_path=config_path,
            restore_step=restore_step,
            state=deepcopy(state)
        )

        # 提前报告不能跨进程序列化的状态，避免只等到超时。
        pickle.dumps(request,protocol=pickle.HIGHEST_PROTOCOL)

        future=self.loop.create_future()
        self.pending[request_id]=future

        try:
            try:
                self.communication.request_queue.put_nowait(request)
            except Full:
                raise RuntimeError("PVE inference queue is full")

            try:
                return await asyncio.wait_for(future,timeout=self.timeout)
            except asyncio.TimeoutError as e:
                raise TimeoutError(f"PVE inference timed out after {self.timeout}s: {config_path}") from e
        finally:
            self.pending.pop(request_id,None)
            if not future.done():
                future.cancel()

    async def stop(self):
        self.fail_pending("PVE inference stopped")

        if self.process is not None:
            if self.process.is_alive():
                self.communication.control_queue.put_nowait("stop")
                await asyncio.to_thread(self.process.join,3)

            if self.process.is_alive():
                self.process.terminate()
                await asyncio.to_thread(self.process.join,2)

            if self.process.is_alive():
                self.process.kill()
                await asyncio.to_thread(self.process.join,2)

            if not self.process.is_alive():
                self.process.close()
                self.process=None

        if self.reader is not None:
            await asyncio.to_thread(self.reader.join,1)
            self.reader=None

        if self.communication is not None:
            self.communication.close()
            self.communication=None