"""Модуль с юнит-тестами для функций работы с S3"""
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from app.s3_helpers import upload, generate_presigned_url, delete


@pytest.fixture(name="mock_aioboto3_session")
def mock_aioboto3_session_fixture():
    """Фикстура-мок aioboto3 сессии для работы с S3"""
    with patch("app.s3_helpers.aioboto3.Session") as mock_session:
        mock_s3_client = MagicMock()
        mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client
        yield mock_s3_client


@pytest.mark.asyncio
async def test_upload_success(mock_aioboto3_session):
    """Тест на загрузку объекта в S3 без ошибок"""
    mock_aioboto3_session.put_object = AsyncMock(return_value="success")
    response = await upload("test_key", b"test_data", "test_bucket")
    assert response == "s3://test_key"
    mock_aioboto3_session.put_object.assert_called_once_with(Bucket="test_bucket", Key="test_key", Body=b"test_data")


@pytest.mark.asyncio
async def test_generate_presigned_url_success(mock_aioboto3_session):
    """Тест на генерацию пресайнед URL для объекта в S3"""
    expected_url = "https://test.url"
    mock_aioboto3_session.generate_presigned_url = AsyncMock(return_value=expected_url)
    response = await generate_presigned_url("test_key", "test_bucket")
    assert response == expected_url
    mock_aioboto3_session.generate_presigned_url.assert_called_once_with(
        "get_object", Params={"Bucket": "test_bucket", "Key": "test_key"}, ExpiresIn=3600
    )


@pytest.mark.asyncio
async def test_delete_success(mock_aioboto3_session):
    """Тест на удаление объекта из S3"""
    mock_aioboto3_session.delete_object = AsyncMock(return_value="success")
    await delete("test_key", "test_bucket")
    mock_aioboto3_session.delete_object.assert_called_once_with(Bucket="test_bucket", Key="test_key")
