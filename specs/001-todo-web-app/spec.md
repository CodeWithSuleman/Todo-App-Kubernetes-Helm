# Feature Specification: Spec-1 Backend + Database Foundation

**Feature Branch**: `001-todo-web-app`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Backend + Database Foundation for Todo Web Application

Target audience:
- Backend developers integrating with the todo API
- System architects evaluating backend infrastructure
- AI agents executing spec-driven implementation (Claude Code)

Primary objective:
Prepare backend infrastructure ONLY for later specs, focusing on FastAPI backend, SQLModel database layer, Neon PostgreSQL connection, and JWT verification middleware.

Scope focus:
- Backend service foundation with proper structure
- Database schema with todos table only (no users table)
- JWT verification middleware (extraction from 'sub' field only)
- Neon PostgreSQL connection and configuration
- Environment-based configuration management
- Clean, professional backend structure ready for consumption

Success criteria:
- Backend service runs properly with configuration
- Database connects to Neon PostgreSQL successfully
- JWT verification extracts user_id from 'sub' field and rejects invalid tokens
- Todos table supports CRUD operations with user_id filtering
- All database queries properly filter by user_id for data isolation
- Environment variables properly configured for deployment

Functional requirements:
- RESTful API endpoints for task CRUD operations (GET, POST, PUT, DELETE, PATCH)
- Task completion toggle endpoint
- Per-user task filtering at database query level
- JWT token verification (no auth flows - only verification)
- Extract user_id from JWT 'sub' field
- Reject invalid/missing tokens with 401 Unauthorized

Non-functional requirements:
- Clean separation of concerns in backend architecture
- Stateless JWT verification (no backend session storage)
- Consistent API response structures
- Proper HTTP status codes and error handling
- Environment-variable-based configuration
- Ready for integration with frontend in Spec-2

Constraints:
- Backend: Python FastAPI (no frontend code)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: JWT verification only (no signup/login flows)
- No user table or credential storage
- No Better Auth configuration logic
- No manual code writing or edits allowed

Timeline:
- Designed for hackathon Phase-II delivery
- All specs, plans, and implementations must be reviewable

Not building:
- Frontend code (Next.js, pages, components, UI)
- Signup / login endpoints
- Better Auth configuration logic
- User table or credential storage
- Any UI-related files
- Complete authentication flows
- User registration or login functionality
