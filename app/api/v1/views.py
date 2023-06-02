from app.api.v1.caching import (
    get_cached_last_scans,
    get_cached_scans,
    get_non_cached_projects,
)
from app.api.v1.models import Projects
from app.api.v1.response import Response
from app.api.v1.services import get_all_projects, get_last_scan, get_projects, get_scans
from app.config.settings import settings


async def resumo_consolidado_projetos_view():
    # Coleta informações dos projetos
    projects = await get_projects(f"{settings.checkmarx_domain}/api/projects")
    if projects.totalCount > len(projects.projects):
        projects = await get_all_projects(
            f"{settings.checkmarx_domain}/api/projects", projects
        )
    non_cached_projects, is_cached = await get_non_cached_projects(projects)

    # Buscar apenas projetos novos que não estão no cache, manter um cache de 60s, pra facilitar e deixar a api mais rapida
    # Busca os ultimos scans
    last_scans = await get_last_scan(
        f"{settings.checkmarx_domain}/api/projects/last-scan",
        [project.id for project in non_cached_projects.projects],
    )
    last_scans = await get_cached_last_scans(last_scans)

    non_cached_projects.add_last_scans(last_scans)

    # Busca o resumo dos scans
    scans = await get_scans(
        f"{settings.checkmarx_domain}/api/scan-summary",
        non_cached_projects.get_projects_scans_id(),
    )
    scans = await get_cached_scans(scans.dict())

    # Soma os projetos em cache com os novos
    if is_cached:
        projects_list = non_cached_projects.projects + projects.projects
        projects = Projects(projects=projects_list, totalCount=len(projects_list))
        projects.add_last_scans(last_scans)

    # Buscar os scans do cache
    # Consolida informações e retorna
    return Response(projects=projects, scans=scans).data
