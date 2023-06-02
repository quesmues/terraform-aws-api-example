from random import randrange

import pytest


@pytest.fixture
def tag_fixture() -> dict:
    return {"priority": "teste"}


@pytest.fixture
def lastscan_fixture() -> dict:
    return {
        "id": "teste",
        "engines": ["teste"],
        "initiator": "teste",
        "createdAt": "teste",
        "updatedAt": "teste",
    }


@pytest.fixture
def project_fixture(lastscan_fixture, tag_fixture) -> dict:
    return {
        "id": "teste",
        "last_scan": lastscan_fixture,
        "name": "teste",
        "criticality": randrange(0, 5),
        "tags": tag_fixture,
    }


@pytest.fixture
def projects_fixture(project_fixture) -> dict:
    return {"totalCount": randrange(0, 1000), "projects": [project_fixture]}


@pytest.fixture
def severity_counters_fixture() -> dict:
    return {"severity": "teste", "counter": randrange(0, 100)}


@pytest.fixture
def counters_fixture(severity_counters_fixture) -> dict:
    return {
        "severityCounters": [severity_counters_fixture],
        "totalCounter": randrange(0, 100),
    }


@pytest.fixture
def scansummary_fixture(counters_fixture) -> dict:
    return {
        "scanId": "teste",
        "sastCounters": counters_fixture,
        "kicsCounters": counters_fixture,
        "scaCounters": counters_fixture,
        "counters": ["scaCounters", "sastCounters", "kicsCounters"],
    }


@pytest.fixture
def scansummaries_fixture(scansummary_fixture) -> dict:
    return {
        "scansSummaries": [scansummary_fixture],
        "totalCount": randrange(0, 100),
    }


@pytest.fixture
def ultimoscan_fixture() -> dict:
    return {"usuario": "teste", "criadoEm": "teste", "atualizadoEm": "teste"}


@pytest.fixture
def resumoprojeto_fixture(ultimoscan_fixture) -> dict:
    return {
        "nomeProjeto": "teste",
        "vulnerabilidadesTotais": randrange(0, 1000),
        "vulnerabilidadesTotaisPorSeveridade": {"teste": randrange(0, 100)},
        "severidade": randrange(0, 5),
        "tiposScan": ["teste"],
        "ultimoScan": ultimoscan_fixture,
    }
