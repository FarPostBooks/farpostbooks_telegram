from typing import List

from farpostbooks_telegram.settings import settings

MODELS_MODULES: List[str] = [
    "farpostbooks_telegram.models.users",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
