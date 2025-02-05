import os
from typing import Final

OPENAPI_SECRET_KEY: Final[str] = os.environ["OPENAI_API_KEY"]

ORGANIZATION_ID: Final[str | None] = os.environ.get("OPENAI_ORGANIZATION_ID", None)

PROJECT_ID: Final[str | None] = os.environ.get("OPENAI_PROJECT_ID", None)
