"""
Document processing service that orchestrates file parsing, embedding generation,
and MongoDB storage.
"""

from typing import Tuple
from datetime import datetime
from app.models.document import DocumentInDB, DocumentResponse
from app.services.file_parser import file_parser
from app.services.embedding_service import embedding_service
from app.services.mongodb_service import mongodb_service


class DocumentService:
    """
    Orchestrates the complete document processing pipeline:
    1. Parse file content
    2. Generate embeddings
    3. Store in MongoDB
    """

    async def process_and_store_document(
        self, file_content: bytes, filename: str
    ) -> Tuple[str, DocumentResponse]:
        """
        Process a file through the complete pipeline.

        Args:
            file_content: Raw file bytes
            filename: Original filename

        Returns:
            Tuple[str, DocumentResponse]: Document ID and response object

        Raises:
            ValueError: If file processing fails
            Exception: If database operation fails
        """
        try:
            # Step 1: Parse the file to extract text
            print(f"📄 Parsing file: {filename}")
            parsed_text = await file_parser.parse_file(file_content, filename)

            if not parsed_text or len(parsed_text.strip()) == 0:
                raise ValueError("No text content could be extracted from the file")

            print(f"✓ Extracted {len(parsed_text)} characters of text")

            # Step 2: Generate embedding from the parsed text
            print(f"🧠 Generating embedding for: {filename}")
            embedding = await embedding_service.generate_embedding(parsed_text)
            embedding_size = embedding_service.get_embedding_size(embedding)

            print(f"✓ Generated embedding with dimension: {embedding_size}")

            # Step 3: Create document object
            document = DocumentInDB(
                file_name=filename,
                file_content=file_content,
                parsed_text=parsed_text,
                embedding=embedding,
                embedding_size=embedding_size,
                created_at=datetime.utcnow(),
            )

            # Step 4: Store in MongoDB
            print(f"💾 Storing document in MongoDB: {filename}")
            document_id = await mongodb_service.insert_document(document.to_dict())

            print(f"✓ Document stored with ID: {document_id}")

            # Step 5: Create response object
            response = DocumentResponse(
                id=document_id,
                file_name=filename,
                parsed_text_preview=parsed_text[:200]
                + ("..." if len(parsed_text) > 200 else ""),
                embedding_size=embedding_size,
                created_at=document.created_at,
            )

            return document_id, response

        except ValueError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            # Wrap other errors with context
            raise Exception(f"Document processing failed: {str(e)}")

    async def get_document(self, document_id: str) -> dict:
        """
        Retrieve a document by ID.

        Args:
            document_id: The document ID

        Returns:
            dict: Document data (without raw file_content for efficiency)
        """
        document = await mongodb_service.get_document(document_id)

        if not document:
            raise ValueError(f"Document not found: {document_id}")

        # Remove file_content from response for efficiency
        # (it can be large, include only if specifically needed)
        document_response = {
            "id": str(document["_id"]),
            "file_name": document.get("file_name"),
            "parsed_text_preview": document.get("parsed_text", "")[:200] + "...",
            "embedding_size": document.get("embedding_size"),
            "created_at": document.get("created_at"),
        }

        return document_response

    async def list_documents(self, limit: int = 100) -> list[dict]:
        """
        List recent documents.

        Args:
            limit: Maximum number of documents to return

        Returns:
            list: List of document summaries
        """
        documents = await mongodb_service.list_documents(limit)

        return [
            {
                "id": str(doc["_id"]),
                "file_name": doc.get("file_name"),
                "parsed_text_preview": doc.get("parsed_text", "")[:100] + "...",
                "embedding_size": doc.get("embedding_size"),
                "created_at": doc.get("created_at"),
            }
            for doc in documents
        ]


# Global document service instance
document_service = DocumentService()
