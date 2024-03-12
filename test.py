import asyncio

class AsyncGameTimer:
    def __init__(self):
        self._time = 0  # 计时器时间，单位为秒
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            await asyncio.sleep(1)
            self._time += 1
            print(f"Timer: {self._time} seconds")

    def stop(self):
        self._running = False

async def game_logic(timer):
    # 异步启动计时器
    asyncio.create_task(timer.start())

    # 模拟其他游戏逻辑
    print("Game started")
    await asyncio.sleep(5)  # 假设游戏逻辑运行了5秒
    print("Game ended")

    # 停止计时器
    timer.stop()
    

async def main():
    timer = AsyncGameTimer()
    await game_logic(timer)

asyncio.run(main())