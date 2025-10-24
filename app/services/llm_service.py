"""
LLM service for generating text responses.
Connects to LM Studio or other OpenAI-compatible endpoints.
"""

from typing import List, Dict, Any
from openai import AsyncOpenAI
from app.config import config


class LLMService:
    """Service for generating text responses using LLM."""

    def __init__(self):
        """Initialize the OpenAI client with custom base URL."""
        self.client = AsyncOpenAI(
            base_url=config.ai.base_url,
            api_key="not-needed",  # LM Studio doesn't require API key
        )
        self.model = config.ai.model_name

    async def generate_response(
        self,
        user_query: str,
        context_documents: List[Dict[str, Any]],
        system_prompt: str = None,
    ) -> str:
        """
        Generate a response using the LLM with retrieved context.

        Args:
            user_query: The user's question
            context_documents: List of relevant documents from vector search
            system_prompt: Optional custom system prompt

        Returns:
            str: Generated response from the LLM
        """
        try:
            # Build context from retrieved documents
            context_text = self._build_context(context_documents)

            # Default system prompt if none provided
            if system_prompt is None:
                system_prompt = (
                    "You are a helpful assistant that answers questions based on the provided context. "
                    "Use the context documents to answer the user's question accurately. "
                    "If the context doesn't contain enough information to answer the question, "
                    "say so honestly and provide what information you can."
                )

            # Build the prompt with context
            user_prompt = f"""Context documents:
{context_text}

User question: {user_query}

Please answer the question based on the context provided above."""

            # Call the LLM
            print(f"🤖 Generating LLM response for: {user_query}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            generated_text = response.choices[0].message.content

            print(f"✓ Generated response ({len(generated_text)} characters)")

            return generated_text

        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")

    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Build context text from retrieved documents.

        Args:
            documents: List of documents with parsed_text_preview

        Returns:
            str: Formatted context text
        """
        if not documents:
            return "No relevant documents found."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            file_name = doc.get("file_name", "Unknown")
            preview = doc.get("parsed_text_preview", "")
            score = doc.get("similarity_score", 0.0)

            context_parts.append(
                f"Document {i} (from {file_name}, relevance: {score:.3f}):\n{preview}\n"
            )

        return "\n".join(context_parts)


# Global LLM service instance
llm_service = LLMService()
