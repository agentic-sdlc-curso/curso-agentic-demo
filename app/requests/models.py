"""Pydantic models of the service requests module."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

RequestStatus = Literal["open", "in_progress", "closed"]

# Strict: only JSON strings are accepted. Whitespace is stripped before the length limits apply.
TitleText = Annotated[
    str, StringConstraints(strict=True, strip_whitespace=True, min_length=1, max_length=100)
]
DescriptionText = Annotated[
    str, StringConstraints(strict=True, strip_whitespace=True, min_length=1, max_length=1000)
]


class ServiceRequestCreate(BaseModel):
    """Body of POST /requests. Extra fields are ignored."""

    title: TitleText = Field(
        description="Surrounding spaces are trimmed first; then 1 to 100 characters are allowed."
    )
    description: DescriptionText = Field(
        description="Surrounding spaces are trimmed first; then 1 to 1000 characters are allowed."
    )


class ServiceRequest(BaseModel):
    """A service request, as stored and returned by the API."""

    id: str
    title: str
    description: str
    status: RequestStatus
    created_at: str
