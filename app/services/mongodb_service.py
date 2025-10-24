"""
MongoDB service for document storage and retrieval.
Uses Motor for async MongoDB operations.
"""

from typing import Optional, Dict, Any
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from datetime import datetime
from app.config import config


class MongoDBService:
    """Service for managing MongoDB connections and operations."""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None

    async def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(config.mongo.url)
            self.db = self.client[config.mongo.database]
            self.collection = self.db[config.mongo.collection]

            # Test the connection
            await self.client.admin.command("ping")
            print(
                f"✓ Connected to MongoDB: {config.mongo.database}/{config.mongo.collection}"
            )
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("✓ Disconnected from MongoDB")

    async def insert_document(self, document: Dict[str, Any]) -> str:
        """
        Insert a document into MongoDB.

        Args:
            document: Document data to insert

        Returns:
            str: The inserted document's ID
        """
        if self.collection is None:
            raise RuntimeError("MongoDB not connected. Call connect() first.")

        # Add timestamp if not present
        if "created_at" not in document:
            document["created_at"] = datetime.utcnow()

        result = await self.collection.insert_one(document)
        return str(result.inserted_id)

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by ID.

        Args:
            document_id: The document ID to retrieve

        Returns:
            Optional[Dict]: The document if found, None otherwise
        """
        if self.collection is None:
            raise RuntimeError("MongoDB not connected. Call connect() first.")

        from bson import ObjectId

        try:
            document = await self.collection.find_one({"_id": ObjectId(document_id)})
            return document
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None

    async def list_documents(self, limit: int = 100) -> list[Dict[str, Any]]:
        """
        List documents from the collection.

        Args:
            limit: Maximum number of documents to return

        Returns:
            list: List of documents
        """
        if self.collection is None:
            raise RuntimeError("MongoDB not connected. Call connect() first.")

        cursor = self.collection.find().sort("created_at", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        return documents


# Global MongoDB service instance
mongodb_service = MongoDBService()
