from typing import Dict, List, Union

from pydantic import BaseModel


class Tag(BaseModel):
    priority: str = ""


class LastScan(BaseModel):
    id: str
    engines: List[str]
    initiator: str
    createdAt: str
    updatedAt: str


class Project(BaseModel):
    id: str
    last_scan: LastScan | None = None
    name: str
    criticality: int = 0
    tags: Tag


class Projects(BaseModel):
    totalCount: int
    projects: List[Project] | None = None

    def add_last_scans(self, last_scans: Dict) -> None:
        for project in self.projects:
            last_scan = last_scans.get(project.id, {})
            project.last_scan = LastScan(**last_scan) if last_scan else None

    def get_projects_scans_id(self) -> List[str]:
        return [project.last_scan.id for project in self.projects if project.last_scan]


class SeverityCounters(BaseModel):
    severity: str
    counter: int


class Counters(BaseModel):
    severityCounters: List[SeverityCounters] | None = None
    totalCounter: int = 0


class ScanSummary(BaseModel):
    scanId: str
    sastCounters: Counters | None = None
    kicsCounters: Counters | None = None
    scaCounters: Counters | None = None
    counters: List[str] = ["scaCounters", "sastCounters", "kicsCounters"]

    def get_total(self) -> int:
        total = 0
        for counter in self.counters:
            total += getattr(self, counter).totalCounter
        return total

    @staticmethod
    def _sum_severities(severities: List[Dict], total: Dict):
        for severity in severities:
            if severity.severity not in total.keys():
                total[severity.severity] = 0
            total[severity.severity] += severity.counter

    def get_total_severity(self) -> dict:
        total = {}
        for counter in self.counters:
            severities = getattr(self, counter).severityCounters
            self._sum_severities(severities, total)
        return total


class ScansSummaries(BaseModel):
    scansSummaries: List[ScanSummary] | None = None
    totalCount: int

    def get_scan(self, last_scan: LastScan) -> Union[ScanSummary, None]:
        if not last_scan:
            return None
        for scan in self.scansSummaries:
            if scan.scanId == last_scan.id:
                return scan
        return None


class UltimoScan(BaseModel):
    usuario: str
    criadoEm: str
    atualizadoEm: str


class ResumoProjeto(BaseModel):
    nomeProjeto: str = ""
    vulnerabilidadesTotais: int = 0
    vulnerabilidadesTotaisPorSeveridade: dict = {}
    severidade: int = 0
    tiposScan: List[str] = [""]
    ultimoScan: UltimoScan | Dict = {}
