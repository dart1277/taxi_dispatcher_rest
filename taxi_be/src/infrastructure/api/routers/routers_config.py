from infrastructure.api.routers.orders.order import router as order_router
from infrastructure.api.routers.taxis.taxi import router as taxi_router
from infrastructure.api.routers.trips.trip import router as trip_router


def add_routers(app) -> None:
    app.include_router(order_router)
    app.include_router(trip_router)
    app.include_router(taxi_router)
