"""Reusable async helpers."""
from __future__ import annotations
import asyncio
from typing import Awaitable, Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def gather_with_concurrency(n: int, *tasks: Awaitable[T]) -> list[T]:
    """asyncio.gather() with a max concurrency cap."""
    sem = asyncio.Semaphore(n)

    async def _wrap(task: Awaitable[T]) -> T:
        async with sem:
            return await task

    return await asyncio.gather(*[_wrap(t) for t in tasks])


async def map_async(
    fn: Callable[[T], Awaitable[R]], items: Iterable[T], concurrency: int = 8
) -> list[R]:
    return await gather_with_concurrency(concurrency, *(fn(i) for i in items))


async def retry(coro_factory: Callable[[], Awaitable[T]], attempts: int = 3, delay: float = 0.5) -> T:
    last: BaseException | None = None
    for i in range(attempts):
        try:
            return await coro_factory()
        except Exception as e:  # noqa: BLE001
            last = e
            await asyncio.sleep(delay * (2 ** i))
    assert last
    raise last
