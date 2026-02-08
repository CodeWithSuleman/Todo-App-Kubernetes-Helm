# Todo Web Application

A secure, multi-user todo application with JWT authentication and user isolation.

## Features

- User registration and authentication with JWT tokens
- Secure todo management with user isolation
- Session management with token refresh
- Responsive web interface
- Data persistence with Neon PostgreSQL

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based authentication

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the values in .env
   ```

4. Run the application:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Update the values in .env.local
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Login and get JWT token
- `POST /api/v1/refresh` - Refresh JWT token

### Todos
- `GET /api/v1/todos` - Get all todos for the current user
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo
- `PATCH /api/v1/todos/{id}/toggle-complete` - Toggle completion status

## Environment Variables

### Backend
- `DATABASE_URL`: Database connection string
- `NEON_DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `APP_NAME`: Application name (default: Todo Web Application)
- `DEBUG`: Enable debug mode (default: False)

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_JWT_SECRET`: JWT secret (should match backend)

## Security

- JWT-based authentication with expiration
- User isolation - users can only access their own todos
- Passwords are hashed using bcrypt
- Input validation and sanitization
- Secure token storage

## Deployment

The application can be deployed with:
- Backend: Any Python hosting service that supports FastAPI
- Frontend: Vercel, Netlify, or any static hosting service that supports Next.js
- Database: Neon Serverless PostgreSQL