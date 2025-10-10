# AI Service

A FastAPI-based microservice for AI-powered document processing and embedding generation using MongoDB and local AI models.

## Project Overview

This service provides:
- FastAPI REST API for document processing
- MongoDB integration for document storage and retrieval
- AI embeddings generation using local models (via LM Studio)
- Async support with Motor (async MongoDB driver)

## Prerequisites

- Python 3.13+
- [UV](https://docs.astral.sh/uv/) package manager
- MongoDB Atlas account (or local MongoDB instance)
- [LM Studio](https://lmstudio.ai/) (or compatible OpenAI-compatible API endpoint)

## Getting Started

### 1. Clone and Navigate to Project

```bash
cd ai_service
```

### 2. Install Dependencies

UV automatically manages the virtual environment and dependencies:

```bash
uv sync
```

### 3. Environment Configuration

Create a `.env` file in the project root (or copy `.env.example`):

```env
# MongoDB Configuration
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=documents_dev
MONGO_COLLECTION=files_qwen

# AI Model Configuration (LM Studio or compatible endpoint)
BASE_URL=http://127.0.0.1:1234/v1
EMBEDDING_MODEL=qwen3-embedding-8b-dwq:2
MODEL_NAME=openai/gpt-oss-20b
```

**Important**: Never commit your `.env` file with real credentials to version control.

### 4. Run the Development Server

Using UV (recommended - no venv activation needed):

```bash
uv run uvicorn main:app --reload
```

Or manually activate the virtual environment:

```bash
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Access API Documentation

FastAPI automatically generates interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Running Tests

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov
```

### Using UV Commands

UV automatically uses the virtual environment without manual activation:

```bash
uv run python main.py          # Run scripts
uv run uvicorn main:app        # Start server
uv run pytest                  # Run tests
uv add <package>               # Add new dependency
uv remove <package>            # Remove dependency
```

### IDE Setup

For autocomplete and linting, configure your IDE to use the virtual environment:

**VS Code**: Open the `ai_service` folder, then select the Python interpreter:
- Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
- Type "Python: Select Interpreter"
- Choose `.venv/bin/python`

## Project Structure

```
ai_service/
├── .env                 # Environment variables (not in git)
├── .venv/              # Virtual environment (managed by UV)
├── main.py             # FastAPI application entry point
├── pyproject.toml      # Project dependencies and configuration
├── uv.lock             # Locked dependency versions
└── README.md           # This file
```

## Dependencies

Key packages (see `pyproject.toml` for full list):
- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **motor** - Async MongoDB driver
- **pymongo** - MongoDB driver
- **openai** - OpenAI API client (works with compatible endpoints)
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework

## API Endpoints

### Root Endpoint

```
GET /
```

Returns a simple example response:

```json
{
  "GFG Example": "FastAPI"
}
```

## Troubleshooting

### Import Errors

If your IDE shows import errors but code runs fine:
1. Ensure your IDE is using `.venv/bin/python` as the interpreter
2. Restart your IDE after selecting the interpreter
3. Run `uv sync` to ensure dependencies are installed

### MongoDB Connection Issues

- Verify your `MONGO_URL` in `.env` is correct
- Check network connectivity to MongoDB Atlas
- Ensure your IP is whitelisted in MongoDB Atlas Network Access

### LM Studio Connection Issues

- Ensure LM Studio is running and the server is started
- Verify `BASE_URL` matches LM Studio's server address (usually `http://127.0.0.1:1234/v1`)
- Check that the specified models are loaded in LM Studio

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `uv run pytest`
4. Submit a pull request

## License

[Add your license here]
