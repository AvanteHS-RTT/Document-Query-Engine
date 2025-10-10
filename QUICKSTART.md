# Quick Start Guide

Get the AI Service running in 5 minutes.

## 1. Start LM Studio

1. Open LM Studio
2. Load embedding model: `qwen3-embedding-8b-dwq:2`
3. Start the server (should run on `http://127.0.0.1:1234`)

## 2. Verify Environment Variables

Ensure your `.env` file exists with:

```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=documents_dev
MONGO_COLLECTION=files_qwen
BASE_URL=http://127.0.0.1:1234/v1
EMBEDDING_MODEL=qwen3-embedding-8b-dwq:2
MODEL_NAME=openai/gpt-oss-20b
EMBEDDING_DIMENSIONS=1536
```

## 3. Start the Service

```bash
cd ai_service
uv run uvicorn main:app --reload
```

## 4. Test the Service

### Option A: Web Interface (Easiest)

Open browser to: `http://localhost:8000/docs`

### Option B: Test Script

```bash
uv run python test_upload.py
```

### Option C: cURL

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@test_document.txt"
```

## What Happens When You Upload?

```
User uploads file → Parse text → Generate embedding → Store in MongoDB
                ↓              ↓                    ↓
              PDF/TXT      1024-dim vector    All data saved
```

## Available Endpoints

- `POST /api/v1/documents/upload` - Upload a file
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get specific document
- `GET /api/v1/health` - Health check
- `GET /docs` - Interactive API documentation

## Troubleshooting

**Can't connect to MongoDB?**
- Check your `MONGO_URL` in `.env`
- Verify your IP is whitelisted in MongoDB Atlas

**Can't generate embeddings?**
- Make sure LM Studio is running
- Verify the server is started in LM Studio
- Check that the embedding model is loaded

**Import errors in IDE?**
- Point your IDE to `.venv/bin/python`
- Restart your IDE

## Next Steps

1. Test with different file types (PDF, TXT, MD)
2. Upload multiple documents
3. Build search/retrieval functionality
4. Add more file format support

See `TESTING.md` for detailed testing instructions.
