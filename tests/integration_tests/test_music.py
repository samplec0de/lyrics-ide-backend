import uuid

import pytest

from integration_tests.test_client import LyricsClient
from integration_tests.test_client.components.exceptions import MusicNotFoundError, ProjectNotFoundError, \
    PermissionDeniedError
from integration_tests.test_client.components.projects import Project


@pytest.mark.asyncio
async def test_upload_music(new_project: Project, lyrics_client: LyricsClient):
    """Тест загрузки музыки"""
    try:
        project = new_project
        music = await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)

        assert music.url.startswith("https://storage.yandexcloud.net/")
        assert abs(music.duration_seconds - 41.616) < 0.1
        assert music.bpm == 61
        assert music.custom_bpm is None
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_replace_music(new_project: Project, lyrics_client: LyricsClient):
    """Тест замены музыки"""
    try:
        project = new_project
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        music = await lyrics_client.upload_music("test_data/metro_200bpm_5min.mp3", project.project_id)

        assert music.url.startswith("https://storage.yandexcloud.net/")
        assert abs(music.duration_seconds - 300.147) < 0.1
        assert music.bpm == 100
        assert music.custom_bpm is None
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_upload_music_project_not_found(lyrics_client: LyricsClient):
    """Тест загрузки музыки, если проекта нет"""
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.upload_music("test_data/metronome.mp3", uuid.uuid4())


@pytest.mark.asyncio
async def test_upload_music_no_grants(new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient):
    """Тест загрузки музыки без прав"""
    project = new_project
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.upload_music("test_data/metronome.mp3", project.project_id)


@pytest.mark.parametrize("grant_level", ["READ_ONLY", "READ_WRITE"])
@pytest.mark.asyncio
async def test_upload_music_not_owner(
        new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, grant_level: str
):
    """Тест загрузки музыки не владельцем"""
    project = new_project
    share_code = await lyrics_client.get_project_share_code(
        project.project_id, grant_level=grant_level, max_activations=1
    )
    await lyrics_client_b.activate_project_share_code(share_code.grant_code_id)
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.upload_music("test_data/metronome.mp3", project.project_id)


@pytest.mark.asyncio
async def test_delete_music(new_project: Project, lyrics_client: LyricsClient):
    """Тест удаления музыки"""
    project = new_project
    await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
    await lyrics_client.delete_music(project.project_id)

    project = await lyrics_client.get_project(project.project_id)
    assert project.music is None


@pytest.mark.asyncio
async def test_delete_music_not_found(new_project: Project, lyrics_client: LyricsClient):
    """Тест удаления музыки, если ее нет"""
    project = new_project
    with pytest.raises(MusicNotFoundError):
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_delete_music_no_grants(new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient):
    """Тест удаления музыки без прав"""
    project = new_project
    try:
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        with pytest.raises(PermissionDeniedError):
            await lyrics_client_b.delete_music(project.project_id)
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.parametrize("grant_level", ["READ_ONLY", "READ_WRITE"])
@pytest.mark.asyncio
async def test_delete_music_not_owner(
        new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, grant_level: str
):
    """Тест удаления музыки не владельцем"""
    try:
        project = new_project
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        share_code = await lyrics_client.get_project_share_code(
            project.project_id, grant_level=grant_level, max_activations=1
        )
        await lyrics_client_b.activate_project_share_code(share_code.grant_code_id)
        with pytest.raises(PermissionDeniedError):
            await lyrics_client_b.delete_music(project.project_id)
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_get_music(new_project: Project, lyrics_client: LyricsClient):
    """Тест получения музыки"""
    try:
        project = new_project
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        music = await lyrics_client.get_music(project.project_id)

        assert music.url.startswith("https://storage.yandexcloud.net/")
        assert abs(music.duration_seconds - 41.616) < 0.1
        assert music.bpm == 61
        assert music.custom_bpm is None
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_get_music_no_grants(new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient):
    """Тест получения музыки без прав"""
    try:
        project = new_project
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        with pytest.raises(PermissionDeniedError):
            await lyrics_client_b.get_music(project.project_id)
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.parametrize("grant_level", ["READ_ONLY", "READ_WRITE"])
async def test_get_music_not_owner(
        new_project: Project, lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, grant_level: str
):
    """Тест получения музыки не владельцем"""
    try:
        project = new_project
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        share_code = await lyrics_client.get_project_share_code(
            project.project_id, grant_level=grant_level, max_activations=1
        )
        await lyrics_client_b.activate_project_share_code(share_code.grant_code_id)
        await lyrics_client_b.get_music(project.project_id)
    finally:
        await lyrics_client.delete_music(project.project_id)


@pytest.mark.asyncio
async def test_get_music_not_found(new_project: Project, lyrics_client: LyricsClient):
    """Тест получения музыки, если ее нет"""
    project = new_project
    with pytest.raises(MusicNotFoundError):
        await lyrics_client.get_music(project.project_id)


@pytest.mark.asyncio
async def test_get_music_project_not_found(lyrics_client: LyricsClient):
    """Тест получения музыки, если проекта нет"""
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.get_music(uuid.uuid4())


@pytest.mark.asyncio
async def test_set_music_custom_bpm(new_project: Project, lyrics_client):
    """Тест установки BPM у музыки"""
    project = new_project
    try:
        await lyrics_client.upload_music("test_data/metronome.mp3", project.project_id)
        music = await lyrics_client.set_music_custom_bpm(project.project_id, 123)

        assert music.custom_bpm == 123
    finally:
        await lyrics_client.delete_music(project.project_id)
