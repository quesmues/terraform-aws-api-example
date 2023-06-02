from typing import Dict

import pytest

from app.api.v1.caching import (
    get_cached_last_scans,
    get_cached_scans,
    get_non_cached_projects,
)
from app.api.v1.models import LastScan, Projects, ScansSummaries


@pytest.mark.asyncio
async def test_get_non_cached_projects(projects_fixture):
    projects, is_cached = await get_non_cached_projects(Projects(**projects_fixture))
    projects, is_cached = await get_non_cached_projects(Projects(**projects_fixture))

    assert is_cached == True
    assert isinstance(projects, Projects)
    assert len(projects.projects) == 0


@pytest.mark.asyncio
async def test_get_non_cached_last_scans(lastscan_fixture):
    last_scans = await get_cached_last_scans({"1": LastScan(**lastscan_fixture)})
    last_scans = await get_cached_last_scans({"1": LastScan(**lastscan_fixture)})

    assert len(last_scans) >= 1
    assert isinstance(last_scans, Dict)


@pytest.mark.asyncio
async def test_get_non_cached_scans(scansummaries_fixture):
    scans = await get_cached_scans(scansummaries_fixture)
    scans = await get_cached_scans(scansummaries_fixture)

    assert len(scans.scansSummaries) >= 1
    assert isinstance(scans, ScansSummaries)
