from typing import List

from app.api.v1.models import Projects, ResumoProjeto, ScansSummaries, ScanSummary


class Response:
    _results: List[ResumoProjeto] = []

    def __init__(self, projects: Projects, scans: ScansSummaries) -> None:
        self.projects = projects
        self.scans = scans
        self._results = []
        self.mount_data()

    @staticmethod
    def _mount_scan_data(scan: ScanSummary) -> dict:
        return (
            {
                "vulnerabilidadesTotais": scan.get_total(),
                "vulnerabilidadesTotaisPorSeveridade": scan.get_total_severity(),
            }
            if scan
            else {}
        )

    def mount_data(self) -> None:
        for project in self.projects.projects:
            scan = self.scans.get_scan(project.last_scan)
            scan_data = self._mount_scan_data(scan)
            temp = {
                "nomeProjeto": project.name,
                "severidade": project.criticality,
                "tiposScan": project.last_scan.engines if project.last_scan else [],
                "ultimoScan": {
                    "usuario": project.last_scan.initiator,
                    "criadoEm": project.last_scan.createdAt,
                    "atualizadoEm": project.last_scan.updatedAt,
                }
                if project.last_scan
                else {},
            }
            self._results.append(ResumoProjeto(**{**temp, **scan_data}))

    @property
    def data(self) -> List[ResumoProjeto]:
        if not self._results:
            raise AttributeError("Por favor chamar o método self.mount_data antes!")
        return sorted(
            self._results, key=lambda x: x.vulnerabilidadesTotais, reverse=True
        )
