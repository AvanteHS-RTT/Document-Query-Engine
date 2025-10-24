"""
MongoDB Atlas Vector Search service.
Uses Atlas Vector Search for efficient similarity search at scale.
"""

from typing import List, Dict, Any
from app.services.embedding_service import embedding_service
from app.services.mongodb_service import mongodb_service
from app.config import config


class SearchService:
    """Service for performing vector similarity search using MongoDB Atlas Vector Search."""

    def __init__(self):
        """Initialize the search service with config from environment."""
        self.index_name = config.mongo.vector_index_name

    async def search_documents(
        self, query: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query using Atlas Vector Search.

        This uses MongoDB's $vectorSearch aggregation stage for efficient
        similarity search directly in the database.

        Args:
            query: Search query text
            top_k: Number of results to return (default: 5)

        Returns:
            List of documents sorted by similarity score
        """
        try:
            # Step 1: Generate embedding for the query
            print(f"🔍 Searching for: {query}")
            query_embedding = await embedding_service.generate_embedding(query)

            # Step 2: Perform Atlas Vector Search
            if mongodb_service.collection is None:
                raise RuntimeError("MongoDB not connected. Call connect() first.")

            # Atlas Vector Search aggregation pipeline
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": self.index_name,
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": top_k * 10,  # Number of candidates to consider
                        "limit": top_k,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "file_name": 1,
                        "parsed_text": 1,
                        "created_at": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
            ]

            print(f"🔎 Running Atlas Vector Search (index: {self.index_name})")

            # Execute the aggregation
            cursor = mongodb_service.collection.aggregate(pipeline)
            documents = await cursor.to_list(length=top_k)

            if not documents:
                print("⚠ No results found")
                return []

            print(f"✓ Found {len(documents)} relevant documents")

            # Format results
            results = []
            for i, doc in enumerate(documents, 1):
                result = {
                    "id": str(doc["_id"]),
                    "file_name": doc.get("file_name"),
                    "similarity_score": doc.get("score", 0.0),
                    "parsed_text_preview": doc.get("parsed_text", "")[:300]
                    + ("..." if len(doc.get("parsed_text", "")) > 300 else ""),
                    "created_at": doc.get("created_at"),
                }
                results.append(result)

                print(
                    f"  {i}. {result['file_name']} (score: {result['similarity_score']:.4f})"
                )

            return results

        except Exception as e:
            raise Exception(f"Atlas Vector Search failed: {str(e)}")


# Global search service instance
search_service = SearchService()
