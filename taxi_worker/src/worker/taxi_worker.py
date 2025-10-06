import asyncio
import logging
import random
import uuid

import aiohttp

from api.dispatch_api_service import post_status, register_worker, get_taxi_info
from settings.app_settings import settings

log = logging.getLogger("worker")

shutdown_flag = False

from enum import StrEnum

cur_x = random.randint(1, 100)
cur_y = random.randint(1, 100)


class TaxiState(StrEnum):
    OFFLINE = "OFFLINE"
    DELIVERED = "DELIVERED"  # DELIVERED is an alias for IDLE, this might need to be changed in the future
    PENDING_PICKUP = "PENDING_PICKUP"
    PICKUP = "PICKUP"
    DRIVING = "DRIVING"


def handle_shutdown(sig, frame):
    global shutdown_flag
    log.info("Received shutdown signal: %s", sig)
    shutdown_flag = True


def create_travel_context(curr_x: int, curr_y: int) -> dict:
    return {
        "cur_x": curr_x,
        "cur_y": curr_y,
        "status": TaxiState.PENDING_PICKUP,
        "waiting_time_units": None,
        "travel_time_units": None
    }


async def poll_taxi_info(session, worker_id: str) -> dict:
    try:
        return await get_taxi_info(session, worker_id)
    except Exception as e:
        log.warning(" polling failed: %s", e)
        return {}


def get_random_wait_time():
    return random.randint(settings.min_sleep, settings.max_sleep)


async def travel(session: aiohttp.ClientSession, worker_id: str):
    global cur_x
    global cur_y

    log.info(f"Poll {worker_id})")
    info = await poll_taxi_info(session, worker_id)
    if info["cur_order_id"]:
        log.info(f"Staring order id: {info['cur_order_id']}, {info}")
        context = create_travel_context(cur_x, cur_y)
        y_pickup_dist = int(abs(context["cur_y"] - info["src_y"]))
        x_pickup_dist = int(abs(context["cur_x"] - info["src_x"]))

        waiting_time = sum([get_random_wait_time() for _ in range(y_pickup_dist + x_pickup_dist)])
        await asyncio.sleep(waiting_time * 0.01)
        context["waiting_time_units"] = waiting_time
        context["cur_x"] = info["src_x"]
        context["cur_y"] = info["src_y"]
        context["status"] = TaxiState.PICKUP
        await post_status(session, worker_id, context)
        log.info(f"Pickup order id: {info['cur_order_id']}, {info}")

        y_delivery_dist = int(abs(context["cur_y"] - info["dst_y"]))
        x_delivery_dist = int(abs(context["cur_x"] - info["dst_x"]))

        travel_time = sum([get_random_wait_time() for _ in range(x_delivery_dist + y_delivery_dist)])
        await asyncio.sleep(travel_time * 0.01)
        context["travel_time_units"] = travel_time
        context["cur_x"] = info["dst_x"]
        context["cur_y"] = info["dst_y"]
        context["status"] = TaxiState.DELIVERED
        cur_x = context["cur_x"]
        cur_y = context["cur_y"]
        await post_status(session, worker_id, context)
        log.info(f"Deliver order id: {info['cur_order_id']}, {info}, {context}")
        return context
    else:
        return None


async def worker_loop():
    worker_id = settings.hostname or str(uuid.uuid4())

    async with aiohttp.ClientSession() as session:
        try:
            await register_worker(session, worker_id, cur_x, cur_y)
        except Exception as e:
            log.error("Failed to register worker: %s", e)
            return

        while not shutdown_flag:
            try:
                await travel(session, worker_id)
            except Exception as e:
                log.error("Travel execution failed: %s", e)
            await asyncio.sleep(3 * settings.poll_interval)

        context = create_travel_context(cur_x, cur_y)
        context["status"] = TaxiState.OFFLINE
        await post_status(session, worker_id, context)
        log.info("Worker loop exiting")
