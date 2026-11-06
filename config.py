import os

from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_KEY = os.getenv(
    "AZURE_OPENAI_KEY"
)

AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT"
)

AZURE_OPENAI_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)

APP_NAME = os.getenv(
    "APP_NAME",
    "琉琉 AI 主播"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"