import enum
import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.exceptions import PermissionDeniedError, UnAuthorizedError, NotFoundError, \
    ProjectNotFoundError
from integration_tests.test_client.components.grant_level import GrantLevel


class ProjectGrantCode:
    """Код доступа к проекту"""

    def __init__(
        self,
        grant_code_id: str,
        project_id: str,
        issuer_user_id: str,
        level: str,
        max_activations: int,
        current_activations: int,
        is_active: bool,
        created_at: str,
        updated_at: str,
    ):
        self.grant_code_id = uuid.UUID(grant_code_id, version=4)
        self.project_id = uuid.UUID(project_id, version=4)
        self.issuer_user_id = uuid.UUID(issuer_user_id, version=4)
        self.level = GrantLevel(level)
        self.max_activations = max_activations
        self.current_activations = current_activations
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def __eq__(self, other):
        return (
            self.grant_code_id == other.grant_code_id
            and self.project_id == other.project_id
            and self.issuer_user_id == other.issuer_user_id
            and self.level == other.level
            and self.max_activations == other.max_activations
            and self.current_activations == other.current_activations
            and self.is_active == other.is_active
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
        )


class ProjectGrant:
    """Грант доступа к проекту"""

    def __init__(
        self,
        grant_code_id: str,
        project_id: str,
        user_id: str,
        user_email: str,
        level: str,
        is_active: bool,
        created_at: str,
    ):
        self.grant_code_id = uuid.UUID(grant_code_id, version=4)
        self.project_id = uuid.UUID(project_id, version=4)
        self.user_id = uuid.UUID(user_id, version=4)
        self.user_email = user_email
        self.level = GrantLevel(level)
        self.is_active = is_active
        self.created_at = created_at

    def __eq__(self, other):
        return (
            self.grant_code_id == other.grant_code_id
            and self.project_id == other.project_id
            and self.user_id == other.user_id
            and self.user_email == other.user_email
            and self.level == other.level
            and self.is_active == other.is_active
            and self.created_at == other.created_at
        )


class GrantMixin:
    """Миксин для работы с уровнем доступа к проекту"""

    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_project_share_code(
            self, project_id: uuid.UUID, grant_level: str, max_activations: int
    ) -> ProjectGrantCode:
        """Получение кода доступа к проекту"""
        payload = {
            "project_id": project_id,
            "grant_level": grant_level,
            "max_activations": max_activations,
        }
        response = await self.client.get(f"/grant/project/{project_id}", params=payload)
        if response.status_code == 404:
            raise ProjectNotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return ProjectGrantCode(**response.json())

    async def activate_project_share_code(self, grant_code_id: uuid.UUID) -> ProjectGrant:
        """Активация кода доступа к проекту"""
        response = await self.client.get(f"/grant/codes/activate/{grant_code_id}")
        if response.status_code == 404:
            raise ProjectNotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return ProjectGrant(**response.json())

    async def get_project_grants(self, project_id: uuid.UUID) -> list[ProjectGrant]:
        """Получение списка грантов доступа к проекту"""
        response = await self.client.get(f"/grant/project/{project_id}/users")
        if response.status_code == 404:
            raise ProjectNotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return [ProjectGrant(**grant) for grant in response.json()]

    async def revoke_project_access(self, project_id: uuid.UUID, user_id: uuid.UUID) -> ProjectGrant:
        """Отзыв доступа к проекту"""
        response = await self.client.delete(f"/grant/{project_id}/users/{user_id}")
        if response.status_code == 404:
            raise NotFoundError("Project or grant not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return ProjectGrant(**response.json())

    async def get_project_codes(self, project_id: uuid.UUID) -> list[ProjectGrantCode]:
        """Получение списка кодов доступа к проекту"""
        response = await self.client.get(f"/grant/projects/{project_id}/codes")
        if response.status_code == 404:
            raise ProjectNotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return [ProjectGrantCode(**grant) for grant in response.json()]

    async def deactivate_project_grant_code(self, grant_code_id: uuid.UUID) -> None:
        """Деактивация кода доступа к проекту"""
        response = await self.client.delete(f"/grant/codes/{grant_code_id}")
        if response.status_code == 404:
            raise ProjectNotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

    async def update_project_access(self, project_id: uuid.UUID, user_id: uuid.UUID, new_level: str) -> ProjectGrant:
        """Обновление уровня доступа к проекту"""
        payload = {
            "new_level": new_level,
        }
        response = await self.client.patch(f"/grant/{project_id}/users/{user_id}", params=payload)
        if response.status_code == 404:
            raise NotFoundError("Project or grant not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")

        return ProjectGrant(**response.json())

    async def leave_project(self, project_id: uuid.UUID):
        """Покинуть проект"""
        response = await self.client.delete(f"/grant/{project_id}/leave")
        if response.status_code == 404:
            raise NotFoundError("Project not found")
        elif response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        elif response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")
