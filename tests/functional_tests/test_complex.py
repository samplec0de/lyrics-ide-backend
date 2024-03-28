import pytest
from httpx import AsyncClient
from app.api.schemas import ProjectBase, TextVariantIn, TextVariantWithoutID

@pytest.mark.asyncio
async def test_scenario_1(async_client: AsyncClient):
    # Create a new project
    project_data = {"name": "Test Project", "description": "This is a test project"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    project = response.json()

    # Add a text to the project
    text_data = {"project_id": project["project_id"], "name": "Test Text"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    text = response.json()

    # Update the text
    updated_text_data = {"name": "Updated Text"}
    response = await async_client.patch(f"/text/{text['text_id']}", json=updated_text_data)
    assert response.status_code == 200
    updated_text = response.json()
    assert updated_text["name"] == updated_text_data["name"]

    # Delete the project
    response = await async_client.delete(f"/project/{project['project_id']}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_scenario_2(async_client: AsyncClient):
    # Create a new project
    project_data = {"name": "Test Project 2", "description": "This is a test project 2"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    project = response.json()

    # Add a text to the project
    text_data = {"project_id": project["project_id"], "name": "Test Text 2"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    text = response.json()

    # Get the text
    response = await async_client.get(f"/text/{text['text_id']}")
    assert response.status_code == 200
    retrieved_text = response.json()
    assert retrieved_text["name"] == text_data["name"]

    # Delete the text
    response = await async_client.delete(f"/text/{text['text_id']}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_scenario_3(async_client: AsyncClient):
    # Create a new project
    project_data = {"name": "Test Project 3", "description": "This is a test project 3"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    project = response.json()

    # Add a text to the project
    text_data = {"project_id": project["project_id"], "name": "Test Text 3"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    text = response.json()

    # Update the project
    updated_project_data = {"name": "Updated Test Project 3", "description": "This is an updated test project 3"}
    response = await async_client.patch(f"/project/{project['project_id']}", json=updated_project_data)
    assert response.status_code == 200
    updated_project = response.json()
    assert updated_project["name"] == updated_project_data["name"]
    assert updated_project["description"] == updated_project_data["description"]

    # Get the project
    response = await async_client.get(f"/project/{project['project_id']}")
    assert response.status_code == 200
    retrieved_project = response.json()
    assert retrieved_project["name"] == updated_project_data["name"]
    assert retrieved_project["description"] == updated_project_data["description"]

@pytest.mark.asyncio
async def test_scenario_4(async_client: AsyncClient):
    # Create a new project
    project_data = {"name": "Test Project 4", "description": "This is a test project 4"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    project = response.json()

    # Add a text to the project
    text_data = {"project_id": project["project_id"], "name": "Test Text 4"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    text = response.json()

    # Delete the text
    response = await async_client.delete(f"/text/{text['text_id']}")
    assert response.status_code == 200

    # Get the project
    response = await async_client.get(f"/project/{project['project_id']}")
    assert response.status_code == 200
    retrieved_project = response.json()
    assert retrieved_project["name"] == project_data["name"]
    assert retrieved_project["description"] == project_data["description"]

@pytest.mark.asyncio
async def test_scenario_5(async_client: AsyncClient):
    # Create a new project
    project_data = {"name": "Test Project 5", "description": "This is a test project 5"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    project = response.json()

    # Add a text to the project
    text_data = {"project_id": project["project_id"], "name": "Test Text 5"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    text = response.json()

    # Update the text
    updated_text_data = {"name": "Updated Test Text 5"}
    response = await async_client.patch(f"/text/{text['text_id']}", json=updated_text_data)
    assert response.status_code == 200
    updated_text = response.json()
    assert updated_text["name"] == updated_text_data["name"]

    # Get the text
    response = await async_client.get(f"/text/{text['text_id']}")
    assert response.status_code == 200
    retrieved_text = response.json()
    assert retrieved_text["name"] == updated_text_data["name"]
