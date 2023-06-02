from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.security import HTTPBasicCredentials

from app.core.authentication import AWSAuthToken, CheckmarxAuthToken


@patch("app.core.authentication.aiohttp.ClientSession")
@pytest.mark.asyncio
async def test_checkmarxauth(session_mock):
    session = AsyncMock()
    post = AsyncMock()
    json = AsyncMock(return_value={"access_token": "data"})
    post.json = json
    post.raise_for_status = MagicMock()
    session.post.return_value = post

    session_mock.return_value.__aenter__.return_value = session

    token = await CheckmarxAuthToken().get_token()

    assert token == "data"


@patch("app.core.authentication.boto3")
@pytest.mark.asyncio
async def test_awsauth(boto3_mock):
    boto3_mock.return_value = AsyncMock()
    credentials = HTTPBasicCredentials(**{"username": "teste", "password": "teste"})
    await AWSAuthToken().check_credentials(credentials)
