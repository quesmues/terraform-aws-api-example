from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.api.v1 import views
from app.config.settings import settings
from app.core.authentication import AWSAuthToken

router = APIRouter(prefix=settings.prefix_v1)

security = HTTPBasic()


@router.get("/resumo-projetos")
async def resumo_consolidado_projetos(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Resumo consolidado dos projetos do Checkmarx, ordenado por vulnerabilidades totais"""
    await AWSAuthToken().check_credentials(credentials)
    return await views.resumo_consolidado_projetos_view()
