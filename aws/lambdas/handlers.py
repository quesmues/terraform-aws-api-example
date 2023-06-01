import sys

sys.path.insert(0, "python3.10")

import asyncio

from app.api.v1.views import resumo_consolidado_projetos_view


def handler_resumo_consolidado_projetos(event, context):
    _, _ = event, context
    results = asyncio.run(resumo_consolidado_projetos_view())
    results = {"status": 200, "results": [x.dict() for x in results]}
    print(results)
    return results
