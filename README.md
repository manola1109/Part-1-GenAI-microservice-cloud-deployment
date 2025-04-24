# AI Text Summarization Microservice

This microservice provides text summarization capabilities using OpenAI's GPT model, built with FastAPI and optimized for containerized deployment.

## Features

- Text summarization using OpenAI's GPT model
- RESTful API with FastAPI
- Docker containerization
- Health check endpoint
- Configurable summarization parameters

## Prerequisites

- Docker
- OpenAI API key
- Python 3.13 (for local development)

## Setup

1. Clone the repository
2. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running with Docker

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### POST /summarize
Summarizes the provided text.

Request body:
```json
{
    "text": "Your text to summarize here",
    "max_tokens": 150,
    "temperature": 0.7
}
```

### GET /health
Health check endpoint.

## Testing the API

Use curl or any HTTP client:

```bash
curl -X POST http://localhost:8000/summarize \
-H "Content-Type: application/json" \
-d '{"text": "Your text to summarize here"}'
```

## Configuration

The following environment variables can be configured:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Server port (default: 8000)
- `MAX_WORKERS`: Number of worker processes (default: 4)