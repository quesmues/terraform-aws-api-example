import logging
import os
import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings

filepath = pathlib.Path(__file__).resolve().parent.parent

load_dotenv(str(filepath) + "/.env")


class Settings(BaseSettings):
    debug: bool = os.getenv("DEBUG")
    app_name: str = "Checkmarx Vulnerabilidades API"
    prefix_v1: str = "/api/v1"

    checkmarx_domain: str = os.getenv("CHECKMARX_API_DOMAIN")
    checkmarx_api_key: str = os.getenv("CHECKMARX_API_KEY")
    checkmarx_auth_url: str = os.getenv("CHECKMARX_AUTH_URL")

    aws_user_pool_id: str = os.getenv("AWS_USER_POOL_ID")
    aws_client_id: str = os.getenv("AWS_CLIENT_ID")
    aws_client_key: str = os.getenv("AWS_CLIENT_KEY")

    cors_allow_origins: str = os.getenv("AWS_API_KEY")


settings = Settings()

if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
