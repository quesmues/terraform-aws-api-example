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
    # Busca os ultimos scans
    last_scans = await get_last_scan(
        f"{settings.checkmarx_domain}/api/projects/last-scan",
        [project.id for project in projects.projects],
    )
    projects.add_last_scans(last_scans)
    # Busca o resumo dos scans
    scans = await get_scans(
        f"{settings.checkmarx_domain}/api/scan-summary",
        projects.get_projects_scans_id(),
    )

    # Consolida informações e retorna
    return Response(projects=projects, scans=scans).data
