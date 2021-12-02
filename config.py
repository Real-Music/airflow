import os
import sys
from functools import lru_cache

from pydantic import BaseSettings, Field

base_dir = os.path.abspath(sys.path[0])


class FactoryConfig(BaseSettings):
    # Database
    SQLALCHEMY_DATABASE_URL: str = Field(..., env="SQLALCHEMY_DATABASE_URL")

    class Config:
        env_file = os.path.join(base_dir, ".env")


@lru_cache()
def settings():
    return FactoryConfig()


config = settings()
