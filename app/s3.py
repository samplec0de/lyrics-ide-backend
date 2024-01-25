"""Вспомогательные функции для работы с объектным хранилищем"""
import aioboto3

from app.config import settings


async def upload(
    key: str,
    bytes_data: bytes,
    bucket: str = settings.s3_bucket,
) -> str:
    """Загрузка файла на s3"""
    session = aioboto3.Session(
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name="ru-central1",
    )
    async with session.client("s3", endpoint_url="https://storage.yandexcloud.net") as s3_client:
        try:
            print(f"Uploading {key} to s3")
            await s3_client.put_object(Bucket=bucket, Key=key, Body=bytes_data)
            print(f"Finished Uploading {key} to s3")
        except Exception as e:
            print(f"Unable to s3 upload {key}: {e} ({type(e)})")
            return ""

    return f"s3://{key}"


async def generate_presigned_url(
        key: str,
        bucket: str = settings.s3_bucket,
        expiration: int = 3600
):
    """Генерация ссылки на скачивание файла"""
    session = aioboto3.Session(
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name="ru-central1",
    )
    async with session.client("s3", endpoint_url="https://storage.yandexcloud.net") as s3_client:
        response = await s3_client.generate_presigned_url('get_object',
                                                          Params={'Bucket': bucket, 'Key': key},
                                                          ExpiresIn=expiration)
        return response
