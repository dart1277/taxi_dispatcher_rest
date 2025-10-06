import asyncio
import logging
import signal
import sys

from settings.app_settings import settings
from worker.taxi_worker import worker_loop
from worker.taxi_worker import handle_shutdown

log = logging.getLogger("worker")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    stream=sys.stdout,
)


async def main():
    log.info(
        "Starting worker (id=%s, dispatch=%s, min_sleep=%d, max_sleep=%d)",
        settings.hostname,
        settings.dispatch_url,
        settings.min_sleep,
        settings.max_sleep,
    )
    await worker_loop()


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

if __name__ == "__main__":
    asyncio.run(main())

