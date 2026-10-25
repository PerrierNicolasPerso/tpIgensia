import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
AWS_SECRET_ACCESS_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCD"
