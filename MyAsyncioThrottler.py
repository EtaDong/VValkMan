from dataclasses import dataclass
from pydantic import BaseModel, PositiveInt

import asyncio
import time
from types import TracebackType
from typing import Optional, Type


class MyAsyncioThrottler:
    """
    Use standard Python docstrings (Google Style)

    Attributes:
        rate_limit: Maximum requests per second.
        _semaphore: To control concurrency.
        _start_time: To track the time window.
    """

    def __init__(self, rate_limit: int):
        self.rate_limit = rate_limit
        self._semaphore = asyncio.Semaphore(rate_limit)
        # self._interval = 1.0 / rate_limit
        # self._last_request_time = 0.0

    async def __aenter__(self):
        """
        进入 'async with' 块。
        1. 抢占信号量。
        2. 计算时间间隔，确保遵守 QPS 限制。
        """
        start_time = time.time()
        await self._semaphore.acquire()
        end_time = asyncio.get_event_loop.time()

        wait_time = end_time - start_time
        if wait_time > 0:
            await asyncio.sleep(wait_time)

        # now = asyncio.get_event_loop().time()
        # 计算距离上一次请求是否已经过了足够的时间
        # wait_time = self._last_request_time + self._interval - now
        # if wait_time > 0:
        # await asyncio.sleep(wait_time)

        # self._last_request_time = asyncio.get_event_loop().time()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        """退出 'async with' 块，释放信号量。"""
        self._semaphore.release()


async def main():
    throttler = MyAsyncioThrottler(rate_limit=5)

    async def task(i):
        async with throttler:
            print(f"[{time.strftime('%H:%M:%S')}] Task {i} is running")
            await asyncio.sleep(0.1)

    await asyncio.gather(*(task(i) for i in range(15)))


if __name__ == "__main__":
    asyncio.run(main())
