# FastAPI Hexagonal Architecture Template

A modern FastAPI project template following the Hexagonal Architecture (Ports and Adapters) pattern with Pydantic for data validation.

## Features

- **Hexagonal Architecture**: Clean separation of concerns with domain, ports, and adapters
- **FastAPI**: High-performance, easy-to-use web framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: ORM for database interactions
- **Dependency Injection**: Clean and testable code
- **Docker Support**: Easy deployment with Docker and docker-compose
- **UV Package Manager**: Fast dependency management

## Project Structure

```
.
├── app/
│   ├── adapters/            # Adapters (implementations of ports)
│   │   ├── controllers/     # API controllers
│   │   ├── external/        # External service adapters
│   │   └── repositories/    # Database repositories
│   ├── api/                 # API layer
│   │   ├── routes/          # API routes
│   │   ├── dependencies.py  # Dependency injection
│   │   ├── router.py        # Main router
│   │   └── schemas.py       # API schemas
│   ├── core/                # Application core
│   │   ├── domain/          # Domain models
│   │   ├── ports/           # Interface definitions
│   │   ├── services/        # Business logic
│   │   └── config.py        # Application configuration
│   ├── tests/               # Tests
│   └── main.py              # Application entry point
├── .env.example             # Example environment variables
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Project dependencies
└── run.py                   # Script to run the application
```

## Hexagonal Architecture Explained

This project follows the Hexagonal Architecture (also known as Ports and Adapters) pattern:

1. **Core Domain**: The center of the application, containing business logic and domain models.
2. **Ports**: Interfaces that define how the core interacts with the outside world.
3. **Adapters**: Implementations of the ports that connect to external systems.

Benefits:

- **Testability**: Easy to test business logic in isolation
- **Flexibility**: Easy to swap implementations (e.g., database, external services)
- **Maintainability**: Clear separation of concerns

## Getting Started

### Prerequisites

- Python 3.8+
- UV package manager (`pip install uv`)
- Docker and Docker Compose (for containerized deployment)

### Local Development

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd fastapi-hexagonal
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies with UV:

   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

5. Run the application:

   ```bash
   python run.py
   ```

6. Access the API documentation at http://localhost:8000/docs

### Using Docker

1. Build and start the containers:

   ```bash
   docker-compose up -d
   ```

2. Access the API documentation at http://localhost:8000/docs

## Development Guide

### Adding a New Entity

1. Create a domain model in `app/core/domain/`
2. Define a repository port in `app/core/ports/`
3. Create a service in `app/core/services/`
4. Implement the repository in `app/adapters/repositories/`
5. Add API schemas in `app/api/schemas.py`
6. Create API routes in `app/api/routes/`
7. Include the new router in `app/api/router.py`

### Running Tests

```bash
pytest
```

## Deployment

### Docker Deployment

1. Build the Docker image:

   ```bash
   docker build -t fastapi-hexagonal .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env fastapi-hexagonal
   ```

### Kubernetes Deployment

1. Create a Kubernetes deployment:

   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   ```

2. Create a Kubernetes service:
   ```bash
   kubectl apply -f kubernetes/service.yaml
   ```

### Cloud Deployment

#### AWS Elastic Beanstalk

1. Install the EB CLI:

   ```bash
   pip install awsebcli
   ```

2. Initialize EB:

   ```bash
   eb init
   ```

3. Create an environment:

   ```bash
   eb create
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

#### Heroku

1. Install the Heroku CLI:

   ```bash
   npm install -g heroku
   ```

2. Login to Heroku:

   ```bash
   heroku login
   ```

3. Create a Heroku app:

   ```bash
   heroku create
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

## Best Practices

- Keep the domain models clean and free of infrastructure concerns
- Use dependency injection for clean and testable code
- Write tests for your business logic
- Use Pydantic for data validation
- Follow the Single Responsibility Principle
- Document your code and APIs

## License

This project is licensed under the MIT License - see the LICENSE file for details.
