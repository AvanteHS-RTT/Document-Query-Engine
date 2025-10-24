"""
FastAPI routes for document upload and management.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List
from app.services.document_service import document_service
from app.services.search_service import search_service
from app.services.rag_service import rag_service
from app.models.document import DocumentResponse

router = APIRouter(prefix="/api/v1", tags=["documents"])


@router.post(
    "/documents/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(..., description="File to upload (PDF, TXT, MD)"),
):
    """
    Upload and process a document.

    This endpoint:
    1. Accepts a file upload (PDF, TXT, or MD)
    2. Extracts text content from the file
    3. Generates an embedding vector
    4. Stores everything in MongoDB

    Returns:
        DocumentResponse: Document metadata including ID and embedding size
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided"
            )

        # Check file extension
        allowed_extensions = ["pdf", "txt", "text", "md", "markdown"]
        file_extension = (
            file.filename.lower().split(".")[-1] if "." in file.filename else ""
        )

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
            )

        # Read file content
        file_content = await file.read()

        if len(file_content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty"
            )

        # Process and store document
        document_id, response = await document_service.process_and_store_document(
            file_content=file_content, filename=file.filename
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        )


@router.get("/chat")
async def chat(
    q: str = Query(..., description="Your question", min_length=1),
    top_k: int = Query(5, description="Number of documents to retrieve", ge=1, le=50),
    include_sources: bool = Query(
        True, description="Include source documents in response"
    ),
):
    """
    RAG-powered chat endpoint.

    This endpoint:
    1. Searches for relevant documents using Atlas Vector Search
    2. Sends the documents + question to the LLM
    3. Returns an AI-generated answer with sources

    Args:
        q: Your question
        top_k: Number of documents to retrieve for context (1-50, default: 5)
        include_sources: Whether to include source documents in response

    Returns:
        AI-generated answer with optional source documents
    """
    try:
        result = await rag_service.query(
            user_query=q, top_k=top_k, include_sources=include_sources
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG query failed: {str(e)}",
        )


@router.get("/documents/search")
async def search_documents(
    q: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=50),
):
    """
    Search documents using Atlas Vector Search.

    This endpoint uses MongoDB Atlas Vector Search for efficient similarity search.
    Returns only the search results without LLM generation.

    Args:
        q: Search query text
        top_k: Number of top results to return (1-50, default: 5)

    Returns:
        List of documents ranked by similarity score
    """
    try:
        results = await search_service.search_documents(query=q, top_k=top_k)
        return {"query": q, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.get("/documents")
async def list_documents(limit: int = 100):
    """
    List recent documents.

    Args:
        limit: Maximum number of documents to return (default: 100)

    Returns:
        List of document summaries
    """
    try:
        if limit < 1 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 1000",
            )

        documents = await document_service.list_documents(limit)
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}",
        )


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """
    Retrieve a document by ID.

    Args:
        document_id: MongoDB document ID

    Returns:
        Document metadata and preview (without full file content)
    """
    try:
        document = await document_service.get_document(document_id)
        return document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}",
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Service status
    """
    return {"status": "healthy", "service": "ai-service", "version": "0.1.0"}
