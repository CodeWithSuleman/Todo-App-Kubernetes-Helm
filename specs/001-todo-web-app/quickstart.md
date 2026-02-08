# Quickstart Guide: Backend + Database Foundation

## Prerequisites
- Python 3.9+ for backend
- Poetry for Python dependency management
- PostgreSQL (Neon Serverless) account

## Environment Setup
1. Copy `.env.example` to `.env` in the backend directory
2. Set JWT secret, database URL, and other configuration values
3. Install dependencies for the backend only

## Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `poetry install`
3. Set environment variables in `.env`:
   - `NEON_DATABASE_URL`: Your Neon PostgreSQL connection string
   - `JWT_SECRET_KEY`: Secret key for JWT verification
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
4. Run the backend: `poetry run uvicorn src.main:app --reload`

## Key Endpoints
- Backend API: `http://localhost:8000/api/v1`
- Health check: `http://localhost:8000/health`
- Todos: `/todos`, `/todos/{todo_id}`, `/todos/{todo_id}/toggle-complete`

## JWT Verification
- All todo endpoints require a valid JWT token in Authorization header
- The middleware extracts user_id from the 'sub' field of the JWT
- All database queries are filtered by the extracted user_id for data isolation
- Invalid/missing tokens are rejected with 401 Unauthorized

## Testing
- Backend tests: `poetry run pytest`

## API Documentation
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Deployment
1. Deploy backend to hosting service that supports Python/FastAPI
2. Configure environment variables for production
3. Set up database connection for production

## Troubleshooting
- Ensure JWT_SECRET_KEY is set correctly in the environment
- Verify database connection string format
- Confirm JWT tokens contain 'sub' field with user_id
- Check that all API requests include Authorization header with valid JWT