from typing import Dict, Tuple

from app.api.v1.models import Project, Projects, ScansSummaries
from app.core.caching import cache


async def get_non_cached_projects(projects: Projects) -> Tuple[Projects, bool]:
    result = cache.get("projects")
    is_cached = False
    if result:
        ids = [proj["id"] for proj in result["projects"]]
        p = [Project(**proj) for proj in projects.projects if proj.id not in ids]
        totalCount = len(p)
        is_cached = True
    cache["projects"] = projects.dict()
    return (
        (Projects(projects=p, totalCount=totalCount), is_cached)
        if is_cached
        else (projects, is_cached)
    )


async def get_cached_last_scans(last_scans: dict) -> Dict:
    cached_scans = cache.get("last_scans", {})
    last_scans = {
        **cached_scans,
        **last_scans,
    }
    cache["last_scans"] = last_scans
    return last_scans


async def get_cached_scans(scans: dict) -> ScansSummaries:
    cached_scans = cache.get("scans")
    if cached_scans:
        scans["scansSummaries"] += cached_scans["scansSummaries"]
        scans["totalCount"] = len(scans["scansSummaries"])
    cache["scans"] = scans
    return ScansSummaries(**scans)
