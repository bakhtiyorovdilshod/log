import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from backend.app.main import app


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_rabbit_template(client: AsyncClient, requests_mock):
    response = await client.post("/rabbit_template/create/", json={"name": "state"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Service name created successfully"}

