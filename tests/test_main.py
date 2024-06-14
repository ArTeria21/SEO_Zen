import pytest
from httpx import AsyncClient, ASGITransport
from kernel_app import app  # Импортируем ваше FastAPI приложение
import asyncio

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.mark.anyio
async def test_index():
    asyncio.sleep(15)
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_create_kernel():
    file_path = "tests/testcases/cars_table.csv"  # Убедитесь, что у вас есть тестовый файл
    with open(file_path, "rb") as file:
        transport = ASGITransport(app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            files = {"file": ("cars_table.csv", file, "text/csv")}
            response = await ac.post("/api/create_kernel/", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"

@pytest.mark.anyio
async def test_http_exception_handler():
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/non-existent-path")
    assert response.status_code == 404

@pytest.mark.anyio
async def test_validation_exception_handler():
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/create_kernel/")
    assert response.status_code == 400
