"""Тесты для работы с кодами доступа к проектам"""
import uuid

import pytest

from tests.integration_tests.test_client import LyricsClient
from tests.integration_tests.test_client.components.exceptions import (
    PermissionDeniedError,
    NotFoundError,
    ProjectNotFoundError,
)
from tests.integration_tests.test_client.components.grant_level import GrantLevel
from tests.integration_tests.test_client.components.projects import Project


@pytest.mark.parametrize("level", ["READ_WRITE", "READ_ONLY"])
@pytest.mark.parametrize("max_activations", [1, 2, 100, 10**9])
@pytest.mark.asyncio
async def test_get_project_share_code(
    lyrics_client: LyricsClient,
    new_project: Project,
    level: str,
    max_activations: int,
):
    """Получение кода доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, level, max_activations)

    assert grant_code.project_id == new_project.project_id
    assert grant_code.issuer_user_id == lyrics_client.user_id
    assert grant_code.level == GrantLevel(level)
    assert grant_code.max_activations == max_activations
    assert grant_code.current_activations == 0
    assert grant_code.is_active
    assert grant_code.created_at
    assert grant_code.updated_at


@pytest.mark.asyncio
async def test_activate_project_share_code(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Активация кода доступа к проекту другим пользователем"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    project_grant = await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)

    assert project_grant.project_id == new_project.project_id
    assert project_grant.user_id == lyrics_client_b.user_id
    assert project_grant.user_email == lyrics_client_b.email
    assert project_grant.level == GrantLevel.READ_WRITE
    assert project_grant.is_active
    assert project_grant.created_at
    assert project_grant.grant_code_id == grant_code.grant_code_id


@pytest.mark.asyncio
async def test_activate_project_share_code_self(lyrics_client: LyricsClient, new_project: Project):
    """Активация кода доступа к проекту самим пользователем"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    with pytest.raises(PermissionDeniedError):
        await lyrics_client.activate_project_share_code(grant_code.grant_code_id)


@pytest.mark.asyncio
async def test_activate_project_share_code_not_active(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Активация неактивного кода доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    await lyrics_client.deactivate_project_grant_code(grant_code.grant_code_id)

    with pytest.raises(NotFoundError):
        await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)


@pytest.mark.asyncio
async def test_activate_project_share_code_max_activations(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Превышение максимального количества активаций кода доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)


@pytest.mark.asyncio
async def test_activate_project_share_code_double(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Двойное активирование кода доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 2)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)


@pytest.mark.asyncio
async def test_activate_project_share_code_replace(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Замена доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_ONLY", 1)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)

    grant_code_2 = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    project_grant = await lyrics_client_b.activate_project_share_code(grant_code_2.grant_code_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1
    assert project_grants[0] == project_grant


@pytest.mark.asyncio
async def test_revoke_project_access(lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project):
    """Отзыв доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1
    assert project_grants[0].is_active

    assert lyrics_client_b.user_id is not None
    await lyrics_client.revoke_project_access(new_project.project_id, lyrics_client_b.user_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1
    assert not project_grants[0].is_active


@pytest.mark.asyncio
async def test_revoke_project_access_no_access(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Пользователь не имеет доступа к проекту"""
    assert lyrics_client_b.user_id is not None
    with pytest.raises(NotFoundError):
        await lyrics_client.revoke_project_access(new_project.project_id, lyrics_client_b.user_id)


@pytest.mark.asyncio
async def test_get_project_codes(lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project):
    """Получение списка кодов доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    grant_code_2 = await lyrics_client.get_project_share_code(new_project.project_id, "READ_ONLY", 1)

    grant_codes = await lyrics_client.get_project_codes(new_project.project_id)

    assert len(grant_codes) == 2
    assert grant_code in grant_codes
    assert grant_code_2 in grant_codes


@pytest.mark.asyncio
async def test_update_project_access(lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project):
    """Обновление уровня доступа к проекту"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1
    assert project_grants[0].level == GrantLevel.READ_WRITE

    assert lyrics_client_b.user_id is not None
    project_grant = await lyrics_client.update_project_access(
        new_project.project_id, lyrics_client_b.user_id, "READ_ONLY"
    )

    assert project_grant.level == GrantLevel.READ_ONLY

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1
    assert project_grants[0].level == GrantLevel.READ_ONLY


@pytest.mark.asyncio
async def test_update_project_access_no_access(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Пользователь не имеет доступа к проекту"""
    assert lyrics_client_b.user_id is not None
    with pytest.raises(NotFoundError):
        await lyrics_client.update_project_access(new_project.project_id, lyrics_client_b.user_id, "READ_ONLY")


@pytest.mark.asyncio
async def test_leave_project(lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project):
    """Пользователь покидает проект"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)

    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 1

    await lyrics_client_b.leave_project(new_project.project_id)

    project_grants = await lyrics_client.get_project_grants(new_project.project_id)
    assert len(project_grants) == 0


@pytest.mark.asyncio
async def test_leave_project_owner(lyrics_client: LyricsClient, new_project: Project):
    """Пользователь является владельцем проекта"""
    with pytest.raises(PermissionDeniedError):
        await lyrics_client.leave_project(new_project.project_id)


@pytest.mark.asyncio
async def test_leave_project_no_access(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Пользователь не имеет доступа к проекту"""
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.leave_project(new_project.project_id)


@pytest.mark.asyncio
async def test_deactivate_project_grant_code(lyrics_client: LyricsClient, new_project: Project):
    """Деактивация кода доступа"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)
    await lyrics_client.deactivate_project_grant_code(grant_code.grant_code_id)


@pytest.mark.asyncio
async def test_deactivate_project_grant_code_not_found(lyrics_client: LyricsClient):
    """Код доступа не найден"""
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.deactivate_project_grant_code(uuid.uuid4())


@pytest.mark.asyncio
async def test_deactivate_project_grant_code_not_owner(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Пользователь не является владельцем проекта"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.deactivate_project_grant_code(grant_code.grant_code_id)
