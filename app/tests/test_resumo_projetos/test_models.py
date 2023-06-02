from typing import Dict

from app.api.v1.models import (
    LastScan,
    Projects,
    ResumoProjeto,
    ScansSummaries,
    ScanSummary,
)


def test_model_projects(projects_fixture, lastscan_fixture):
    projects = Projects(**projects_fixture)
    last_scans = {project.id: lastscan_fixture for project in projects.projects}
    projects.add_last_scans(last_scans)

    assert len(projects.projects) >= 1
    assert len(projects.get_projects_scans_id()) >= 1


def test_model_scansummary(scansummary_fixture):
    scansummary = ScanSummary(**scansummary_fixture)
    total = scansummary.get_total()
    total_severity = scansummary.get_total_severity()

    assert scansummary.scanId
    assert isinstance(total, int)
    assert isinstance(total_severity, Dict)


def test_model_scansummaries(scansummaries_fixture, lastscan_fixture):
    scanssummaries = ScansSummaries(**scansummaries_fixture)
    last_scan = LastScan(**lastscan_fixture)
    lastscan_fixture.update({"id": "None"})
    last_scan_empty = LastScan(**lastscan_fixture)
    scan = scanssummaries.get_scan(last_scan)
    scan_none = scanssummaries.get_scan(last_scan_empty)

    assert scanssummaries.scansSummaries
    assert isinstance(scan, ScanSummary)
    assert scan_none == None


def test_model_resumoprojeto(resumoprojeto_fixture):
    resumo = ResumoProjeto(**resumoprojeto_fixture)

    assert resumo.nomeProjeto
