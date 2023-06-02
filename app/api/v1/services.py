import asyncio
import logging
from typing import Any, Dict, List

import aiohttp

from app.api.v1.models import Projects, ScansSummaries
from app.config.settings import settings
from app.core.authentication import CheckmarxAuthToken

auth = CheckmarxAuthToken()


async def _get_data(url: str, **data) -> Dict:
    token = await auth.get_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(
        headers=headers,
    ) as session:
        response = await session.get(url, params=data)
        if settings.debug:
            print(f"Starting request <{response.method} {response.url.path}>")
        response.raise_for_status()
        return await response.json()


async def _gen_offset_results(url: str, offset: int, total_count: int) -> Any:
    count = (total_count // offset) + 1
    tasks = [_get_data(url, offset=offset * x) for x in range(1, count)]
    return await asyncio.gather(*tasks)


async def _gen_multiple_requests(
    url: str, l: List, atrib_name: str, params: dict = {}
) -> Any:
    x = 10
    ids = [l[i * x : (i + 1) * x] for i in range((len(l) + x - 1) // x)]
    tasks = [_get_data(url, **{**{atrib_name: s}, **params}) for s in ids]
    return await asyncio.gather(*tasks)


async def get_projects(url: str) -> Projects:
    data = await _get_data(url)
    return Projects(**data)


async def get_last_scan(url: str, projects_id: List[str]) -> Dict:
    results = await _gen_multiple_requests(url, projects_id, "project-ids")
    data = {}
    for x in results:
        data.update(x)
    return data


async def get_scans(url: str, scans_id: List[str]) -> ScansSummaries:
    params = {
        "include-queries": "false",
        "include-status-counters": "false",
        "include-files": "false",
    }
    results = await _gen_multiple_requests(url, scans_id, "scan-ids", params)
    data = [scan for x in results for scan in x.get("scansSummaries", [])]
    return ScansSummaries(scansSummaries=data, totalCount=len(data))


async def get_all_projects(url: str, projects: Projects) -> Projects:
    results = await _gen_offset_results(
        url, len(projects.projects), projects.totalCount
    )
    results = [x for x in results if x.get("projects", None)]
    data = [
        project for x in results for project in x.get("projects", [])
    ] + projects.projects
    return Projects(totalCount=projects.totalCount, projects=data)
