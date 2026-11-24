"""Business rules of service requests."""

from datetime import UTC, datetime
from uuid import uuid4

from app.requests.models import ServiceRequest, ServiceRequestCreate
from app.requests.repository import RequestRepository


def create_request(data: ServiceRequestCreate, repository: RequestRepository) -> ServiceRequest:
    """Create an open request with a generated id and creation date, and store it."""
    item = ServiceRequest(
        id=str(uuid4()),
        title=data.title,
        description=data.description,
        status="open",
        created_at=datetime.now(UTC).isoformat(),
    )
    return repository.add(item)
