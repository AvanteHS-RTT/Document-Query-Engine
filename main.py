"""
AI Service - FastAPI application for document processing and embedding generation.

This service provides endpoints for:
- Uploading documents (PDF, TXT, MD)
- Extracting text content
- Generating embeddings
- Storing in MongoDB
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import router
from app.services.mongodb_service import mongodb_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    print("🚀 Starting AI Service...")
    await mongodb_service.connect()
    print("✓ AI Service ready")

    yield

    # Shutdown
    print("🛑 Shutting down AI Service...")
    await mongodb_service.disconnect()
    print("✓ AI Service stopped")


# Initialize FastAPI app
app = FastAPI(
    title="AI Document Processing Service",
    description="Service for processing documents, generating embeddings, and storing in MongoDB",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
def root():
    """
    Root endpoint with service information.
    """
    return {
        "service": "AI Document Processing Service",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/api/v1/health",
            "upload": "/api/v1/documents/upload",
            "list": "/api/v1/documents",
            "get": "/api/v1/documents/{document_id}",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
