# Testing the AI Service

This guide will help you test the document upload, embedding generation, and MongoDB storage functionality.

## Prerequisites

Before testing, ensure you have:

1. **MongoDB** - Running and accessible (MongoDB Atlas or local)
2. **LM Studio** - Running with the embedding model loaded
3. **Environment Variables** - Configured in `.env` file

### Starting LM Studio

1. Open LM Studio
2. Load the embedding model: `qwen3-embedding-8b-dwq:2` (or your configured model)
3. Start the local server (usually runs on `http://127.0.0.1:1234`)
4. Verify the server is running by visiting: `http://127.0.0.1:1234/v1/models`

## Running the Service

### Method 1: Using UV (Recommended)

```bash
cd ai_service
uv run uvicorn main:app --reload
```

### Method 2: Manual Activation

```bash
cd ai_service
source .venv/bin/activate
uvicorn main:app --reload
```

The service will start on `http://localhost:8000`

## Testing Methods

### 1. Interactive API Documentation (Easiest)

FastAPI provides automatic interactive documentation:

1. Open your browser to: `http://localhost:8000/docs`
2. Click on `POST /api/v1/documents/upload`
3. Click "Try it out"
4. Upload a test file (PDF or TXT)
5. Click "Execute"
6. View the response with document ID and metadata

### 2. Using the Test Script

A test script is provided to verify all functionality:

```bash
uv run python test_upload.py
```

This script will:
- Create a test document
- Upload it to the service
- Retrieve the document by ID
- List all documents

### 3. Using cURL

#### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_document.txt"
```

#### Get a Document

```bash
curl -X GET "http://localhost:8000/api/v1/documents/{document_id}"
```

#### List Documents

```bash
curl -X GET "http://localhost:8000/api/v1/documents?limit=10"
```

#### Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### 4. Using HTTPie (Alternative)

If you have HTTPie installed:

```bash
# Upload
http -f POST localhost:8000/api/v1/documents/upload file@test_document.txt

# Get document
http GET localhost:8000/api/v1/documents/{document_id}

# List documents
http GET localhost:8000/api/v1/documents limit==10
```

## Expected Response Format

### Successful Upload Response

```json
{
  "id": "507f1f77bcf86cd799439011",
  "file_name": "test_document.txt",
  "parsed_text_preview": "This is a test document...",
  "embedding_size": 1024,
  "created_at": "2024-10-10T12:00:00"
}
```

### Error Responses

#### Invalid File Type
```json
{
  "detail": "Unsupported file type. Allowed: pdf, txt, text, md, markdown"
}
```

#### Empty File
```json
{
  "detail": "File is empty"
}
```

## Verifying MongoDB Storage

You can verify documents are stored in MongoDB:

### Using MongoDB Compass

1. Connect to your MongoDB instance
2. Navigate to your database (e.g., `documents_dev`)
3. Open the collection (e.g., `files_qwen`)
4. View the stored documents with all fields:
   - `file_name`
   - `file_content` (binary)
   - `parsed_text`
   - `embedding` (array of floats)
   - `embedding_size`
   - `created_at`

### Using MongoDB Shell

```javascript
// Connect to your database
use documents_dev

// View recent documents
db.files_qwen.find().sort({created_at: -1}).limit(5).pretty()

// Count documents
db.files_qwen.countDocuments()

// View a specific document (without large fields)
db.files_qwen.findOne(
  {},
  {file_content: 0, embedding: 0}
)
```

## Troubleshooting

### Connection Errors

**MongoDB Connection Failed**
- Check `MONGO_URL` in `.env`
- Verify network connectivity
- Ensure IP is whitelisted in MongoDB Atlas

**LM Studio Connection Failed**
- Ensure LM Studio server is running
- Check `BASE_URL` matches LM Studio's address
- Verify the embedding model is loaded

### File Processing Errors

**"Failed to parse PDF"**
- Ensure the PDF is not corrupted
- Try a different PDF file
- Check the PDF is not password-protected

**"No text content could be extracted"**
- File might be empty
- PDF might be image-based (scanned) without text layer
- Try a text-based PDF or TXT file

### Embedding Errors

**"Failed to generate embedding"**
- LM Studio might not be running
- Model might not be loaded
- Text might be too long (will auto-truncate, but check logs)

## Performance Testing

### Upload Multiple Files

Create a script to upload multiple files:

```python
import asyncio
import httpx
from pathlib import Path

async def upload_files():
    async with httpx.AsyncClient() as client:
        files = Path("test_files").glob("*.txt")
        for file_path in files:
            with open(file_path, 'rb') as f:
                response = await client.post(
                    'http://localhost:8000/api/v1/documents/upload',
                    files={'file': (file_path.name, f, 'text/plain')}
                )
                print(f"{file_path.name}: {response.status_code}")

asyncio.run(upload_files())
```

## Next Steps

After successful testing:

1. Test with various file types (PDF, TXT, MD)
2. Test with different file sizes
3. Verify embedding quality
4. Test concurrent uploads
5. Monitor MongoDB storage usage
6. Test retrieval performance

## Sample Test Files

Create these test files in your project:

### test_small.txt
```
This is a small test document.
```

### test_medium.txt
```
This is a medium-sized test document with multiple paragraphs.

[Add several paragraphs of text]
```

### test_large.pdf
Use any multi-page PDF document for testing.
