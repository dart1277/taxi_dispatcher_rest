import dataclasses
from enum import StrEnum


@dataclasses.dataclass
class Position:
    x: int
    y: int


class TaxiStatus(StrEnum):
    OFFLINE = "OFFLINE"
    DELIVERED = "DELIVERED"  # DELIVERED is an alias for IDLE, this might need to be changed in the future
    PENDING_PICKUP = "PENDING_PICKUP"
    PICKUP = "PICKUP"
    DRIVING = "DRIVING"
