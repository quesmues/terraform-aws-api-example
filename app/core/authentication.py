import base64
import hashlib
import hmac
import logging

import aiohttp
import boto3
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from app.config.settings import settings


class CheckmarxAuthToken:
    url = settings.checkmarx_auth_url
    api_key = settings.checkmarx_api_key

    async def get_token(self) -> str:
        data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": self.api_key,
        }
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, data=data)
            response.raise_for_status()
            data = await response.json()
        return data.get("access_token")


class AWSAuthToken:
    client_id = settings.aws_client_id
    client_key = settings.aws_client_key
    user_pool_id = settings.aws_user_pool_id

    def __init__(self) -> None:
        self.client = boto3.client("cognito-idp")

    async def get_secret_hash(self, username) -> str:
        msg = username + self.client_id
        dig = hmac.new(
            str(self.client_key).encode("utf-8"),
            msg=str(msg).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    async def check_credentials(self, credentials: HTTPBasicCredentials) -> None:
        secret_hash = await self.get_secret_hash(credentials.username)
        try:
            _ = self.client.admin_initiate_auth(
                UserPoolId=self.user_pool_id,
                ClientId=self.client_id,
                AuthFlow="ADMIN_NO_SRP_AUTH",
                AuthParameters={
                    "USERNAME": credentials.username,
                    "SECRET_HASH": secret_hash,
                    "PASSWORD": credentials.password,
                },
                ClientMetadata={
                    "username": credentials.username,
                    "password": credentials.password,
                },
            )
        except (
            self.client.exceptions.NotAuthorizedException,
            self.client.exceptions.UserNotConfirmedException,
            self.client.exceptions.ResourceNotFoundException,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
            )
        except Exception as e:
            if settings.debug:
                logging.debug(f"Error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
