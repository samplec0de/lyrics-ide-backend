"""Клиент TipTap"""
import httpx


class TipTapClient:
    """Клиент TipTap"""

    def __init__(self, app_id: str, api_secret: str):
        self.app_id = app_id
        self.api_secret = api_secret
        self.base_url = f"https://{app_id}.collab.tiptap.cloud"

    async def delete_document(self, document_id: str) -> bool:
        """Удаление документа"""
        url = f"{self.base_url}/documents/{document_id}"
        async with httpx.AsyncClient(headers={"Authorization": f"{self.api_secret}"}) as client:
            response = await client.delete(url)
            return response.status_code == 204
