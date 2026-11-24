"""HTTP routes of service requests."""

from fastapi import APIRouter, status

from app.requests import service
from app.requests.models import ServiceRequest, ServiceRequestCreate
from app.requests.repository import repository

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_request(body: ServiceRequestCreate) -> ServiceRequest:
    return service.create_request(body, repository)
