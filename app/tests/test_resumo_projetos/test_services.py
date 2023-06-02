from typing import Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.api.v1.models import Projects, ScansSummaries
from app.api.v1.services import (
    _gen_multiple_requests,
    _gen_offset_results,
    _get_data,
    get_all_projects,
    get_last_scan,
    get_projects,
    get_scans,
)


@patch("app.api.v1.services.aiohttp.ClientSession")
@patch("app.api.v1.services.auth")
@pytest.mark.asyncio
async def test_get_data(auth_mock, session_mock):
    session = AsyncMock()
    get = AsyncMock()
    json = AsyncMock(return_value={"teste": "data"})
    get.json = json
    get.raise_for_status = MagicMock()
    session.get.return_value = get

    session_mock.return_value.__aenter__.return_value = session
    auth_mock.get_token = AsyncMock()
    results = await _get_data("teste", data="data")

    assert json.call_count >= 1
    assert results == {"teste": "data"}


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_gen_offset_results(get_data_mock):
    get_data_mock.return_value = True
    results = await _gen_offset_results("teste", 10, 20)

    assert len(results) >= 1
    assert results[0] == True


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_gen_multiple_requests(get_data_mock):
    get_data_mock.return_value = True
    results = await _gen_multiple_requests(
        "teste", ["teste"], "teste", {"teste": "teste"}
    )

    assert len(results) >= 1
    assert results[0] == True


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_get_projects(get_data_mock, projects_fixture):
    get_data_mock.return_value = projects_fixture
    results = await get_projects("teste")

    assert isinstance(results, Projects)


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_get_last_scan(get_data_mock, lastscan_fixture):
    get_data_mock.return_value = [{"1": lastscan_fixture, "2": lastscan_fixture}]
    results = await get_last_scan("teste", ["1", "2"])

    assert isinstance(results, Dict)
    assert "1" in results.keys()


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_get_scans(get_data_mock, scansummaries_fixture):
    get_data_mock.return_value = scansummaries_fixture
    results = await get_scans("url", ["1", "2"])

    assert isinstance(results, ScansSummaries)


@patch("app.api.v1.services._get_data")
@pytest.mark.asyncio
async def test_get_all_projects(get_data_mock, project_fixture, projects_fixture):
    get_data_mock.return_value = {"projects": [project_fixture]}
    results = await get_all_projects("url", Projects(**projects_fixture))

    assert isinstance(results, Projects)
