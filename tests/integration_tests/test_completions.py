"""Тесты для автодополнения текста"""
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "text, expected",
    [
        pytest.param("", [], id="empty"),
        pytest.param("Я хочу петь", ["и танцевать!"], id="smoke"),
        pytest.param("Я хочу петь", ["и танцевать!", "с тобой"], id="smoke multi answer"),
        pytest.param("Я хочу\nпеть песни", ["и танцевать!"], id="multiline"),
    ],
)
@pytest.mark.asyncio
async def test_create_completion(authorized_client: AsyncClient, mocker, text: str, expected: list[str]):
    """Тест автодополнения текста"""
    mocker.patch("app.api.routers.completions.get_llm_lyrics_completions", return_value=expected)
    response = await authorized_client.post(
        "/completions/",
        json={"text": text},
    )
    assert response.status_code == 200
    expected_response = [{"completion": completion} for completion in expected]
    assert response.json() == expected_response
