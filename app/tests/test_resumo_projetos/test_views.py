from unittest.mock import patch

import pytest

from app.api.v1.models import Projects, ResumoProjeto, ScansSummaries
from app.api.v1.views import resumo_consolidado_projetos_view


@patch("app.api.v1.views.get_projects")
@patch("app.api.v1.views.get_last_scan")
@patch("app.api.v1.views.get_scans")
@patch("app.api.v1.views.get_all_projects")
@pytest.mark.asyncio
async def test_resumo_consolidado_projetos_view(
    get_all_projects,
    get_scans,
    get_last_scan,
    get_projects,
    projects_fixture,
    lastscan_fixture,
    scansummaries_fixture,
):
    get_all_projects.return_value = Projects(**projects_fixture)
    get_projects.return_value = Projects(**projects_fixture)
    get_last_scan.return_value = {"teste": lastscan_fixture}
    get_scans.return_value = ScansSummaries(**scansummaries_fixture)

    response = await resumo_consolidado_projetos_view()

    assert isinstance(response, list)
    assert isinstance(response[0], ResumoProjeto)
