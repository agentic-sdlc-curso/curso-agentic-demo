"""Tests for H1: create a request (POST /requests)."""

from collections.abc import Iterator
from datetime import datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.requests.repository import repository

URL = "/requests"


@pytest.fixture(autouse=True)
def _empty_repository() -> Iterator[None]:
    repository.clear()
    yield
    repository.clear()


def _body(**overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {"title": "Laptop", "description": "I need a new laptop"}
    body.update(overrides)
    return body


def _without(field: str) -> dict[str, Any]:
    body = _body()
    del body[field]
    return body


def _assert_error(res: Any) -> None:
    assert res.status_code == 400
    assert res.headers["content-type"].startswith("application/json")
    error = res.json()["error"]
    assert isinstance(error, str)
    assert error.strip() != ""


def test_c1_creates_request_with_valid_body(client: TestClient) -> None:
    res = client.post(URL, json=_body())

    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Laptop"
    assert data["description"] == "I need a new laptop"
    assert data["status"] == "open"
    assert isinstance(data["id"], str)
    assert data["id"] != ""
    assert isinstance(data["created_at"], str)
    assert data["created_at"] != ""


def test_c2_trims_title(client: TestClient) -> None:
    res = client.post(URL, json=_body(title="   My  title \t"))

    assert res.status_code == 201
    assert res.json()["title"] == "My  title"


def test_c3_trims_description(client: TestClient) -> None:
    res = client.post(URL, json=_body(description="  \n Some  description  "))

    assert res.status_code == 201
    assert res.json()["description"] == "Some  description"


def test_c4_rejects_missing_title(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_without("title")))


@pytest.mark.parametrize("title", [None, 123, True, ["a"], "", "   ", "\t\n"])
def test_c4_rejects_invalid_title(client: TestClient, title: Any) -> None:
    _assert_error(client.post(URL, json=_body(title=title)))


@pytest.mark.parametrize("length", [1, 100])
def test_c5_accepts_title_length_within_limits(client: TestClient, length: int) -> None:
    title = "a" * length

    res = client.post(URL, json=_body(title=title))

    assert res.status_code == 201
    assert res.json()["title"] == title


def test_c5_accepts_title_of_100_characters_after_trimming(client: TestClient) -> None:
    title = "a" * 100

    res = client.post(URL, json=_body(title=f"  {title}  "))

    assert res.status_code == 201
    assert res.json()["title"] == title


def test_c5_rejects_title_of_101_characters(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_body(title="a" * 101)))


def test_c5_rejects_title_of_101_characters_after_trimming(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_body(title=f"  {'a' * 101}  ")))


def test_c6_rejects_missing_description(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_without("description")))


@pytest.mark.parametrize("description", [None, 123, True, ["a"], "", "   ", "\t\n"])
def test_c6_rejects_invalid_description(client: TestClient, description: Any) -> None:
    _assert_error(client.post(URL, json=_body(description=description)))


@pytest.mark.parametrize("length", [1, 1000])
def test_c7_accepts_description_length_within_limits(client: TestClient, length: int) -> None:
    description = "a" * length

    res = client.post(URL, json=_body(description=description))

    assert res.status_code == 201
    assert res.json()["description"] == description


def test_c7_accepts_description_of_1000_characters_after_trimming(client: TestClient) -> None:
    description = "a" * 1000

    res = client.post(URL, json=_body(description=f"  {description}  "))

    assert res.status_code == 201
    assert res.json()["description"] == description


def test_c7_rejects_description_of_1001_characters(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_body(description="a" * 1001)))


def test_c7_rejects_description_of_1001_characters_after_trimming(client: TestClient) -> None:
    _assert_error(client.post(URL, json=_body(description=f"  {'a' * 1001}  ")))


def test_c8_ignores_extra_fields(client: TestClient) -> None:
    res = client.post(
        URL,
        json=_body(extra_field="x", status="closed", id="forced-id", created_at="2000-01-01"),
    )

    assert res.status_code == 201
    data = res.json()
    assert "extra_field" not in data
    assert data["status"] == "open"
    assert data["id"] != "forced-id"
    assert data["created_at"] != "2000-01-01"
    assert set(data) == {"id", "title", "description", "status", "created_at"}


def test_c9_ids_are_unique_and_dates_are_iso_8601_with_timezone(client: TestClient) -> None:
    first = client.post(URL, json=_body(title="First"))
    second = client.post(URL, json=_body(title="Second"))

    assert first.status_code == 201
    assert second.status_code == 201
    first_data = first.json()
    second_data = second.json()
    assert first_data["id"] != ""
    assert second_data["id"] != ""
    assert first_data["id"] != second_data["id"]
    for data in (first_data, second_data):
        created_at = datetime.fromisoformat(data["created_at"])
        assert created_at.tzinfo is not None
        assert created_at.utcoffset() is not None


def test_c10_rejects_malformed_json(client: TestClient) -> None:
    res = client.post(URL, content="{ not json", headers={"Content-Type": "application/json"})

    _assert_error(res)


def test_c10_rejects_non_object_json_body(client: TestClient) -> None:
    res = client.post(URL, content="[1, 2]", headers={"Content-Type": "application/json"})

    _assert_error(res)
