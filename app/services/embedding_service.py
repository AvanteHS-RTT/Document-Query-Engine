"""
Embedding generation service using OpenAI-compatible API.
Connects to LM Studio or other compatible endpoints for generating embeddings.
"""

from typing import List
from openai import AsyncOpenAI
from app.config import config


class EmbeddingService:
    """Service for generating text embeddings using AI models."""

    def __init__(self):
        """Initialize the OpenAI client with custom base URL."""
        self.client = AsyncOpenAI(
            base_url=config.ai.base_url,
            api_key="not-needed",  # LM Studio doesn't require API key
        )
        self.model = config.ai.embedding_model
        self.dimensions = (
            config.ai.embedding_dimensions
        )  # Configurable, defaults to 1536 for ada-002 compatibility

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for the given text.

        Args:
            text: Text content to generate embedding for

        Returns:
            List[float]: Embedding vector (1536 dimensions by default)

        Raises:
            Exception: If embedding generation fails
        """
        try:
            # Clean and truncate text if too long
            cleaned_text = text.strip()

            # Most embedding models have token limits (e.g., 8192 tokens)
            # Roughly estimate: 1 token ≈ 4 characters
            max_chars = 30000  # Conservative limit for ~8k tokens
            if len(cleaned_text) > max_chars:
                cleaned_text = cleaned_text[:max_chars]
                print(f"⚠ Text truncated from {len(text)} to {max_chars} characters")

            response = await self.client.embeddings.create(
                input=cleaned_text,
                model=self.model,
                dimensions=self.dimensions,  # Request specific dimensions for compatibility
            )

            embedding = response.data[0].embedding

            # Verify we got the expected dimension
            if len(embedding) != self.dimensions:
                print(
                    f"⚠ Warning: Expected {self.dimensions} dimensions, got {len(embedding)}"
                )

            return embedding

        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")

    def get_embedding_size(self, embedding: List[float]) -> int:
        """
        Get the size/dimension of the embedding vector.

        Args:
            embedding: The embedding vector

        Returns:
            int: Dimension of the embedding
        """
        return len(embedding)


# Global embedding service instance
embedding_service = EmbeddingService()
