from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.v1.routes.AWSAuthToken")
@patch("app.api.v1.routes.views.resumo_consolidado_projetos_view")
def test_read_main(views_mock, aws_mock):
    aws_mock.return_value = AsyncMock()
    views_mock.return_value = {"teste": "teste"}
    response = client.get("/api/v1/resumo-projetos", auth=("teste", "teste"))
    assert response.status_code == 200
