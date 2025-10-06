import logging

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from settings.app_settings import settings

log = logging.getLogger("dispatch_api")


def retry_policy():
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )


@retry_policy()
async def post_status(session: aiohttp.ClientSession, worker_id: str, payload: dict):
    url = f"{settings.dispatch_url.rstrip('/')}/taxi/status/{worker_id}"
    async with session.put(url, json=payload, timeout=settings.http_timeout) as resp:
        text = await resp.text()
        if resp.status >= 400:
            raise Exception(f"PUT {url} failed {resp.status}: {text}")
        log.info("Status posted: %s", payload)
        return resp.status, text


@retry_policy()
async def get_taxi_info(session: aiohttp.ClientSession, worker_id: str):
    url = f"{settings.dispatch_url.rstrip('/')}/taxi/{worker_id}"
    async with session.get(url, timeout=settings.http_timeout) as resp:
        if resp.status == 200:
            return await resp.json()
        return None


@retry_policy()
async def register_worker(session: aiohttp.ClientSession, worker_id: str, cur_x: int, cur_y: int):
    url = f"{settings.dispatch_url.rstrip('/')}/taxi/register/{worker_id}"
    async with session.post(url, timeout=settings.http_timeout, json={"cur_x": cur_x, "cur_y": cur_y}) as resp:
        if resp.status >= 400:
            raise Exception(f"Registration failed: {resp.status} {await resp.text()}")
    log.info("Worker %s registered successfully", worker_id)
