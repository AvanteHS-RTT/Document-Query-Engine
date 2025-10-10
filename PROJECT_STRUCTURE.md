# Project Structure

```
ai_service/
├── app/
│   ├── __init__.py
│   ├── config.py                    # Environment configuration loader
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py              # Pydantic models for documents
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mongodb_service.py       # MongoDB connection & operations
│   │   ├── file_parser.py           # PDF/TXT text extraction
│   │   ├── embedding_service.py     # AI embedding generation
│   │   └── document_service.py      # Orchestrates complete pipeline
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                # FastAPI endpoints
│   │
│   └── utils/
│       └── __init__.py
│
├── uploads/                          # Temporary file storage (gitignored)
├── .venv/                            # Virtual environment (gitignored)
├── .env                              # Environment variables (gitignored)
├── .gitignore
├── main.py                           # FastAPI application entry point
├── test_upload.py                    # Test script for uploads
├── pyproject.toml                    # Dependencies and project config
├── uv.lock                           # Locked dependency versions
├── README.md                         # Main documentation
├── QUICKSTART.md                     # Quick start guide
├── TESTING.md                        # Testing instructions
└── PROJECT_STRUCTURE.md              # This file
```

## Module Descriptions

### Core Application (`app/`)

#### `config.py`
- Loads environment variables from `.env`
- Provides typed configuration classes
- Global config instance for app-wide access

#### `models/document.py`
- `DocumentCreate` - Input schema for document creation
- `DocumentResponse` - API response schema
- `DocumentInDB` - Complete document schema for MongoDB

#### `services/mongodb_service.py`
- Manages MongoDB connection lifecycle
- Async operations with Motor
- CRUD operations for documents

#### `services/file_parser.py`
- Extracts text from PDF files (using pypdf)
- Handles plain text files with encoding detection
- Extensible for additional file formats

#### `services/embedding_service.py`
- Connects to OpenAI-compatible API (LM Studio)
- Generates embedding vectors from text
- Handles text truncation for token limits

#### `services/document_service.py`
- Orchestrates the complete pipeline:
  1. Parse file → extract text
  2. Generate embedding
  3. Store in MongoDB
- Provides document retrieval and listing

#### `api/routes.py`
- FastAPI endpoint definitions
- Request validation
- Error handling
- Response formatting

### Main Application (`main.py`)

- FastAPI app initialization
- Lifespan management (startup/shutdown)
- MongoDB connection on startup
- CORS configuration
- Router registration

## Data Flow

### Document Upload Pipeline

```
1. Client Upload
   ↓
2. FastAPI Route (/api/v1/documents/upload)
   ↓
3. File Validation (extension, size)
   ↓
4. Document Service (document_service.py)
   ├─→ File Parser (file_parser.py)
   │   └─→ Extract text from PDF/TXT
   ├─→ Embedding Service (embedding_service.py)
   │   └─→ Generate embedding vector
   └─→ MongoDB Service (mongodb_service.py)
       └─→ Store in database
   ↓
5. Response to Client
```

### Document Structure in MongoDB

```json
{
  "_id": "507f1f77bcf86cd799439011",
  "file_name": "document.pdf",
  "file_content": "<binary data>",
  "parsed_text": "Full extracted text...",
  "embedding": [0.123, 0.456, ...],  // 1024+ dimensions
  "embedding_size": 1024,
  "created_at": "2024-10-10T12:00:00Z"
}
```

## Configuration Files

### `.env`
Environment variables for:
- MongoDB connection
- AI model endpoints
- Service configuration

### `pyproject.toml`
Project metadata and dependencies:
- FastAPI framework
- MongoDB drivers (motor, pymongo)
- OpenAI client
- File parsing (pypdf)
- Testing tools (pytest)

### `.gitignore`
Excludes from version control:
- Virtual environments
- Environment variables
- Uploaded files
- Python cache files

## Testing Files

### `test_upload.py`
- Automated test for upload pipeline
- Tests upload, retrieval, and listing
- Verifies end-to-end functionality

### `TESTING.md`
- Comprehensive testing guide
- Multiple testing methods
- Troubleshooting tips

## Extension Points

### Adding New File Types

Edit `app/services/file_parser.py`:

```python
@staticmethod
async def parse_docx(file_content: bytes) -> str:
    # Add DOCX parsing logic
    pass
```

### Adding New Endpoints

Edit `app/api/routes.py`:

```python
@router.post("/documents/search")
async def search_documents(query: str):
    # Add search functionality
    pass
```

### Custom Processing

Edit `app/services/document_service.py`:

```python
async def process_with_chunking(self, file_content: bytes, filename: str):
    # Add chunking logic for large documents
    pass
```
