"""
RAG (Retrieval-Augmented Generation) service.
Combines vector search with LLM generation for contextual responses.
"""

from typing import Dict, Any
from app.services.search_service import search_service
from app.services.llm_service import llm_service


class RAGService:
    """Service for performing RAG: search + LLM generation."""

    async def query(
        self, user_query: str, top_k: int = 5, include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Perform a RAG query: search for relevant documents and generate a response.

        Args:
            user_query: The user's question
            top_k: Number of documents to retrieve (default: 5)
            include_sources: Whether to include source documents in response

        Returns:
            Dict containing:
                - answer: Generated response from LLM
                - sources: List of source documents (if include_sources=True)
                - query: Original query
        """
        try:
            print(f"\n{'=' * 70}")
            print(f"RAG Query: {user_query}")
            print(f"{'=' * 70}\n")

            # Step 1: Retrieve relevant documents
            print("Step 1: Retrieving relevant documents...")
            documents = await search_service.search_documents(
                query=user_query, top_k=top_k
            )

            if not documents:
                return {
                    "query": user_query,
                    "answer": "I couldn't find any relevant documents to answer your question.",
                    "sources": [],
                }

            print(f"✓ Retrieved {len(documents)} documents\n")

            # Step 2: Generate response using LLM
            print("Step 2: Generating LLM response...")
            answer = await llm_service.generate_response(
                user_query=user_query, context_documents=documents
            )

            print(f"✓ Response generated\n")
            print(f"{'=' * 70}\n")

            # Step 3: Build response
            result = {
                "query": user_query,
                "answer": answer,
            }

            if include_sources:
                result["sources"] = documents

            return result

        except Exception as e:
            raise Exception(f"RAG query failed: {str(e)}")


# Global RAG service instance
rag_service = RAGService()
