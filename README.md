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

## Code Organization & Naming Conventions

### Directory & File Organization Rules

1. **Follow Single Responsibility Principle**:

   - Each module should have a single responsibility
   - Each directory should contain related functionality

2. **Directory Naming**:

   - Use lowercase, singular nouns for directories (e.g., `domain`, `service`, `repository`)
   - Use plural only for collections of similar items (e.g., `routes`, `controllers`)
   - Avoid abbreviations in directory names

3. **File Naming**:

   - Use snake_case for all Python files (e.g., `item_service.py`)
   - Use descriptive names that indicate functionality (e.g., `sqlalchemy_item_repository.py`)
   - Prefix implementation files with their type (e.g., `sqlalchemy_` for SQLAlchemy implementations)
   - Keep filenames short but descriptive

4. **Module Organization**:
   - Group related functionality in the same module
   - Create new modules when functionality becomes too complex
   - Use `__init__.py` files to expose only what's necessary

### Python Naming Conventions

1. **Variables and Functions**:

   - Use snake_case for variable and function names (e.g., `item_id`, `get_item`)
   - Use descriptive names that indicate purpose (e.g., `active_users` instead of `users1`)
   - Prefix private variables/functions with underscore (e.g., `_validate_item`)

2. **Classes**:

   - Use PascalCase (CapWords) for class names (e.g., `ItemService`, `Repository`)
   - Use noun or noun phrases for class names
   - Suffix implementation classes with their type (e.g., `SQLAlchemyItemRepository`)

3. **Constants**:

   - Use UPPERCASE_WITH_UNDERSCORES for constants (e.g., `MAX_ITEMS`, `DEFAULT_TIMEOUT`)
   - Place constants in a dedicated module or at the top of the relevant file

4. **Type Hints**:
   - Always use type hints for function arguments and return values
   - Use descriptive type variable names (e.g., `T` for generic types)

### Hexagonal Architecture Specific Rules

1. **Domain Models**:

   - Place all domain models in `app/core/domain/`
   - Keep domain models free of infrastructure concerns
   - Use dataclasses or Pydantic models for domain entities
   - Name domain models as nouns representing the entity (e.g., `Item`, `User`)

2. **Ports (Interfaces)**:

   - Place all interfaces in `app/core/ports/`
   - Name interfaces descriptively (e.g., `Repository`, `ItemRepository`)
   - Suffix repository interfaces with "Repository" (e.g., `ItemRepository`)
   - Suffix service ports with "Service" (e.g., `PaymentService`)

3. **Adapters (Implementations)**:

   - Place all implementations in `app/adapters/` with appropriate subdirectories
   - Prefix implementation classes with their type (e.g., `SQLAlchemyItemRepository`)
   - Group adapters by their external system (e.g., `repositories`, `external`)

4. **Services**:
   - Place all business logic in `app/core/services/`
   - Suffix service implementations with "Service" (e.g., `ItemService`)
   - Services should depend on ports, not concrete implementations

### API Layer Rules

1. **Routes**:

   - Group routes by resource in separate modules (e.g., `items.py`, `users.py`)
   - Use plural resource names for route collections
   - Prefix route function names with HTTP method (e.g., `get_item`, `create_item`)

2. **Schemas**:

   - Group related schemas together
   - Suffix request schemas with purpose (e.g., `ItemCreate`, `ItemUpdate`)
   - Suffix response schemas with "Response" (e.g., `ItemResponse`)
   - Inherit from base schemas to maintain consistency

3. **Dependencies**:
   - Prefix dependency functions with "get\_" (e.g., `get_item_service`)
   - Keep dependencies simple and focused on a single responsibility

### General Code Style Guidelines

1. **Documentation**:

   - Document all public functions, classes, and modules
   - Use docstrings following Google style format
   - Include type information in docstrings
   - Document complex algorithms and business rules

2. **Imports**:

   - Order imports: standard library, third-party, local application
   - Use absolute imports instead of relative imports
   - Import only what you need (avoid `from module import *`)

3. **Error Handling**:

   - Use custom exceptions for domain-specific errors
   - Handle exceptions at appropriate levels
   - Log exceptions with context information
   - Return appropriate HTTP status codes in API responses

4. **Testing**:
   - Name test files with `test_` prefix (e.g., `test_item_service.py`)
   - Group tests by unit/component being tested
   - Test each layer of the hexagonal architecture independently

### Project Growth Guidelines

1. **When to Split Files**:

   - Split files when they exceed 300-500 lines
   - Split when a file handles more than one logical entity
   - Create new modules when functionality becomes complex

2. **When to Create New Services**:

   - Create a new service when functionality crosses domain boundaries
   - Extract a service when a single service handles too many responsibilities

3. **When to Create New Ports**:
   - Create a new port when interacting with a new external system
   - Create specialized ports for specific domain needs

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

## Troubleshooting

### Docker Credential Errors

If you encounter the following error when using Docker:

```
error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH, out: ``
```

This occurs when Docker is trying to use the Docker Desktop credential helper but can't find it in your system's PATH. Try one of these solutions:

1. **Update Docker Desktop** if you're using it, ensuring it's properly installed.

2. **Configure Docker to use a different credential store**:
   Edit or create the file `~/.docker/config.json` with the following content:

   ```json
   {
     "credsStore": "",
     "credHelpers": {}
   }
   ```

   This tells Docker not to use any credential helper.

3. **For macOS users**:

   ```bash
   # Install the osxkeychain credential helper
   brew install docker-credential-helper-osxkeychain

   # Update Docker config
   echo '{"credsStore":"osxkeychain"}' > ~/.docker/config.json
   ```

4. **For Linux users**:

   ```bash
   # Use the secretservice credential helper
   apt-get install pass gnupg2

   # Update Docker config
   echo '{"credsStore":"secretservice"}' > ~/.docker/config.json
   ```

5. **Simplest solution** - Remove the credsStore field entirely:
   ```bash
   # Create or modify ~/.docker/config.json
   echo '{}' > ~/.docker/config.json
   ```

After applying any of these fixes, try your Docker command again.

### Pydantic Settings Errors

If you encounter errors related to parsing settings when starting the application, such as:

```
error parsing value for field "ALLOWED_HOSTS" from source "EnvSettingsSource"
```

This is typically due to environment variables format issues. Here are some solutions:

1. **ALLOWED_HOSTS format issue**:

   The error occurs because `ALLOWED_HOSTS` is defined as a `List[str]` in the code, but is provided as a comma-separated string in the environment.

   Fixed by modifying your `.env` file or environment variables:

   ```
   # Incorrect format
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Correct format - use JSON array format
   ALLOWED_HOSTS=["localhost","127.0.0.1"]
   ```

2. **Alternative solution - Update the config.py**:

   You can modify the `app/core/config.py` file to handle string conversions automatically:

   ```python
   @validator("ALLOWED_HOSTS", pre=True)
   def assemble_allowed_hosts(cls, v: Union[str, List]) -> List[str]:
       if isinstance(v, str) and not v.startswith("["):
           return [host.strip() for host in v.split(",")]
       elif isinstance(v, str):
           return json.loads(v)
       return v
   ```

3. **For Docker environment**:

   In `docker-compose.yml`, you can set the variable directly:

   ```yaml
   environment:
     - ALLOWED_HOSTS=["localhost","127.0.0.1","api"]
   ```

4. **Simplest solution for development**:

   Set `ALLOWED_HOSTS` to accept all hosts during development:

   ```
   ALLOWED_HOSTS=["*"]
   ```

Remember to restart your application after making these changes.

### PostgreSQL Connection Issues

If you encounter errors related to PostgreSQL connections, such as:

```
ModuleNotFoundError: No module named 'psycopg2'
```

or other database connection errors, try these solutions:

1. **Install PostgreSQL adapter**:

   Make sure you have the required PostgreSQL adapter installed:

   ```bash
   pip install psycopg2-binary
   # or with uv:
   uv pip install psycopg2-binary
   ```

2. **Check Database URL format**:

   Ensure your `DATABASE_URL` in the `.env` file has the correct format:

   ```
   # For PostgreSQL
   DATABASE_URL=postgresql://username:password@hostname:port/database_name

   # Example
   DATABASE_URL=postgresql://postgres:postgres@db:5432/app
   ```

3. **For Docker environments**:

   - Ensure the database is running before the API service
   - Check that the database hostname in `DATABASE_URL` matches the service name in `docker-compose.yml`
   - Wait for the database to be ready before connecting:

   ```yaml
   # In docker-compose.yml
   api:
     depends_on:
       db:
         condition: service_healthy
   db:
     healthcheck:
       test: ["CMD-SHELL", "pg_isready -U postgres"]
       interval: 5s
       timeout: 5s
       retries: 5
   ```

4. **Install system dependencies**:

   If using a custom environment or Docker, ensure you have the required system libraries:

   ```bash
   # For Debian/Ubuntu
   apt-get install -y libpq-dev postgresql-client

   # For Alpine
   apk add --no-cache postgresql-dev
   ```

5. **Use SQLAlchemy async driver**:

   Update your `DATABASE_URL` to use an async driver:

   ```
   # Async PostgreSQL driver
   DATABASE_URL=postgresql+asyncpg://username:password@hostname:port/database_name
   ```

   And install the driver:

   ```bash
   pip install asyncpg
   ```

For any other database issues, check the PostgreSQL logs and ensure your database server is properly configured.

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
