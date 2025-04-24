# AI Text Summarization Microservice

**Last Updated:** 2025-04-24 10:15:53 UTC  
**Maintainer:** manola1109

## Project Overview

This microservice provides AI-powered text summarization capabilities using OpenAI's GPT model. It's built with FastAPI, containerized with Docker, and deployable to AWS using Kubernetes.

## Features

- Text summarization using OpenAI's GPT model
- RESTful API endpoints
- Docker containerization
- Kubernetes deployment configuration
- CI/CD pipeline with GitHub Actions
- AWS cloud deployment
- Automatic scaling capabilities
- Health monitoring

## Tech Stack

- Python 3.11
- FastAPI
- OpenAI API
- Docker
- Kubernetes
- AWS (EKS, ECR)
- GitHub Actions
- Terraform

## Getting Started

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/manola1109/ai-summarizer.git
cd ai-summarizer
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
uvicorn app:app --reload
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t summarizer-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your_api_key_here summarizer-api
```

### Cloud Deployment

1. Configure AWS credentials:
```bash
aws configure
```

2. Deploy infrastructure with Terraform:
```bash
cd terraform
terraform init
terraform apply
```

3. Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
```

## API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|---------|------------|
| `/` | GET | Root endpoint - API information |
| `/health` | GET | Health check endpoint |
| `/summarize` | POST | Text summarization endpoint |
| `/docs` | GET | OpenAPI documentation |

### Summarize Endpoint

**Request:**
```json
POST /summarize
{
    "text": "Your text to summarize goes here",
    "max_tokens": 150,
    "temperature": 0.7
}
```

**Response:**
```json
{
    "summary": "Summarized text",
    "original_length": 100,
    "summary_length": 50,
    "created_at": "2025-04-24T10:15:53"
}
```

## Project Structure

```
.
├── app.py                 # Main FastAPI application
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── README.md            # Project documentation
├── .gitignore           # Git ignore file
├── tests/               # Test files
├── k8s/                # Kubernetes configurations
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
├── terraform/           # Infrastructure as Code
│   └── main.tf
└── .github/
    └── workflows/
        └── ci-cd.yml    # CI/CD pipeline
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Application port (default: 8000)
- `MAX_WORKERS`: Number of worker processes (default: 4)
- `ENVIRONMENT`: Development/Production

### Kubernetes Resources

- CPU Request: 250m
- CPU Limit: 500m
- Memory Request: 512Mi
- Memory Limit: 1Gi

## Monitoring and Scaling

- Liveness Probe: `/health` endpoint
- Readiness Probe: `/health` endpoint
- HorizontalPodAutoscaler: Scales based on CPU utilization
- Resource monitoring through Kubernetes dashboard

## CI/CD Pipeline

1. **Test Stage**
   - Run unit tests
   - Generate coverage report
   - Upload coverage to Codecov

2. **Build Stage**
   - Build Docker image
   - Push to Amazon ECR

3. **Deploy Stage**
   - Deploy to EKS cluster
   - Verify deployment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainer:
- GitHub: [@manola1109](https://github.com/manola1109)

## Acknowledgments

- OpenAI for providing the GPT API
- FastAPI framework developers
- AWS for cloud infrastructure
- Kubernetes community
