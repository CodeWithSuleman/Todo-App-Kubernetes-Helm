---
id: 0001
title: Update Project Constitution with Detailed Principles
stage: constitution
date: 2026-01-28
surface: agent
model: gemini-pro
feature: "none"
branch: "none"
user: "none"
command: "/sp.constitution"
labels: [constitution, setup]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  - "none"
---

## Prompt

/sp.constitution

Project: Full-Stack Multi-User Todo Web Application (Agentic Dev Stack)

Core principles:
- Specification-driven development (no manual coding)
- Security-first architecture (JWT-based authentication & authorization)
- Clear separation of concerns (frontend, backend, auth, data)
- Deterministic, reproducible agent execution
- Production-readiness over demo-only shortcuts

Key standards:
- All features must be traceable to written specifications
- REST API must strictly follow defined endpoints and HTTP semantics
- Authentication must be enforced on every protected route
- User data isolation must be guaranteed at the API and database level
- All generated code must align with the declared tech stack only

Technology constraints:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- No additional frameworks or auth systems allowed

Security standards:
- All API endpoints require valid JWT authentication
- JWT verification must occur server-side in FastAPI
- Shared secret must be sourced from environment variables
- User ID from JWT must match route-level user context
- Unauthorized requests return HTTP 401
- Cross-user data access is strictly forbidden

Development constraints:
- No manual code edits allowed (Claude Code only)
- Development must follow:
  Spec → Plan → Tasks → Implementation
- Each phase must be reviewable and auditable
- Backend and frontend must operate as independent services
- Stateless authentication (no backend session storage)

Functional requirements:
- Implement all 5 Basic Level Todo features
- Persistent storage using PostgreSQL
- RESTful CRUD operations for tasks
- Task ownership enforced on every operation
- Responsive, multi-user frontend interface

Quality requirements:
- Code must be readable, modular, and maintainable
- API responses must use consistent schemas
- Proper error handling and status codes required
- Database migrations must be deterministic
- Environment-based configuration (no hardcoded secrets)

Success criteria:
- All specs fully implemented without deviations
- All API endpoints secured and functional
- Users can only access their own tasks
- JWT-based authentication verified end-to-end
- Application runs successfully in a real deployment environment
- Project demonstrates a complete Agentic Dev Stack workflow

## Response snapshot

I have updated the project constitution in `.specify/memory/constitution.md` to version 1.0.0, incorporating the detailed principles and standards you provided.

I also updated the plan template at `.specify/templates/plan-template.md` to align with the new constitution, specifically in the "Technical Context" and "Constitution Check" sections. The spec and tasks templates were already aligned with the new principles and did not require changes.

## Outcome

- ✅ Impact: High - establishes the foundational principles for the project.
- 🧪 Tests: n/a
- 📁 Files: Updated the constitution and the plan template.
- 🔁 Next prompts: /sp.specify to start a new feature.
- 🧠 Reflection: The `create-phr.sh` script did not create the directory structure as expected. I had to create the `history/prompts/constitution` directory manually.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` script did not create the necessary directories.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a