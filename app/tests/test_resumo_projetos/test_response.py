from typing import List

from app.api.v1.models import Projects, ResumoProjeto, ScansSummaries
from app.api.v1.response import Response


def test_response(lastscan_fixture, projects_fixture, scansummaries_fixture):
    projects = Projects(**projects_fixture)
    last_scans = {project.id: lastscan_fixture for project in projects.projects}
    projects.add_last_scans(last_scans)
    scans = ScansSummaries(**scansummaries_fixture)
    response = Response(projects=projects, scans=scans).data

    assert isinstance(response, list)
    assert len(response) > 0
    assert isinstance(response[0], ResumoProjeto)
