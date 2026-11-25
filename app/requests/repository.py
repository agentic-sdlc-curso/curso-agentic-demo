"""In-memory storage of service requests."""

from app.requests.models import ServiceRequest


class RequestRepository:
    def __init__(self) -> None:
        self._items: dict[str, ServiceRequest] = {}

    def add(self, item: ServiceRequest) -> ServiceRequest:
        self._items[item.id] = item
        return item

    def clear(self) -> None:
        self._items.clear()


repository = RequestRepository()
