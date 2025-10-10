"""
Configuration management for the AI Service.
Loads environment variables and provides typed configuration.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class MongoConfig:
    """MongoDB configuration settings."""

    url: str
    database: str
    collection: str

    @classmethod
    def from_env(cls) -> "MongoConfig":
        """Load MongoDB config from environment variables."""
        return cls(
            url=os.getenv("MONGO_URL", ""),
            database=os.getenv("MONGO_DB", "documents_dev"),
            collection=os.getenv("MONGO_COLLECTION", "files_qwen"),
        )


@dataclass
class AIConfig:
    """AI model configuration settings."""

    base_url: str
    embedding_model: str
    model_name: str
    embedding_dimensions: int

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Load AI config from environment variables."""
        return cls(
            base_url=os.getenv("BASE_URL", "http://127.0.0.1:1234/v1"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "qwen3-embedding-8b-dwq:2"),
            model_name=os.getenv("MODEL_NAME", "openai/gpt-oss-20b"),
            embedding_dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "1536")),
        )


@dataclass
class AppConfig:
    """Application configuration."""

    mongo: MongoConfig
    ai: AIConfig
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB default

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load full app config from environment variables."""
        return cls(
            mongo=MongoConfig.from_env(),
            ai=AIConfig.from_env(),
        )


# Global config instance
config = AppConfig.from_env()
