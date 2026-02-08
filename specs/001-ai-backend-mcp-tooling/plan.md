# Implementation Plan: AI Backend & MCP Tooling

**Branch**: `001-ai-backend-mcp-tooling` | **Date**: 2026-02-05 | **Spec**: specs/001-ai-backend-mcp-tooling/spec.md
**Input**: Feature specification from `/specs/001-ai-backend-mcp-tooling/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a stateless AI-powered backend that enables natural-language todo management using OpenAI Agents SDK and MCP (Model Context Protocol), exposing task operations as secure, deterministic tools. The system will provide a single POST chat endpoint that processes natural language requests through an AI agent that selects appropriate MCP tools for task operations while maintaining strict user isolation and stateless operation.

## Technical Context

**Frontend**: Next.js 16+ (App Router)
**Backend**: Python FastAPI
**ORM**: SQLModel
**Database**: Neon Serverless PostgreSQL
**Authentication**: Better Auth (JWT-based)
**AI Framework**: OpenAI Agents SDK
**MCP Framework**: Official MCP SDK
**Testing**: pytest
**Target Platform**: Web
**Performance Goals**: <2 seconds for all chat requests with appropriate authentication and authorization
**Constraints**: Adherence to REST API contract, Stateless authentication, All state changes must occur only through MCP tools
**Scale/Scope**: Multi-user system supporting secure user isolation for todo management

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Specification-driven**: Does this plan directly map to a `spec.md`?
- [x] **Security-first**: Does the plan include JWT authentication for all protected routes?
- [x] **Separation of Concerns**: Is there a clear boundary between frontend, backend, and data layers?
- [x] **Reproducible Agent Execution**: Is the plan detailed enough for an agent to execute without ambiguity?
- [x] **Production-ready**: Does the plan avoid demo-only shortcuts?
- [x] **Traceable**: Are all features traceable to written specifications?
- [x] **Strict REST API**: Does the plan adhere to the defined API endpoints and HTTP semantics?
- [x] **Enforced Authentication**: Is authentication enforced on every protected route?
- [x] **User Data Isolation**: Is user data isolation guaranteed at the API and database level?
- [x] **Declared Tech Stack**: Does the plan only use the approved tech stack (Next.js, FastAPI, SQLModel, Neon, Better Auth)?

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── todo.py
│   │   ├── user.py
│   │   └── conversation.py          # NEW: Conversation model
│   │   └── message.py               # NEW: Message model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── todo_service.py
│   │   └── conversation_service.py  # NEW: Conversation service
│   ├── api/
│   │   ├── __init__.py
│   │   ├── todos.py
│   │   ├── auth.py
│   │   └── chat.py                  # NEW: Chat API endpoints
│   ├── mcp/
│   │   ├── __init__.py              # NEW: MCP server module
│   │   ├── server.py                # NEW: MCP server implementation
│   │   └── tools.py                 # NEW: MCP tool definitions
│   ├── agents/
│   │   ├── __init__.py              # NEW: AI agent module
│   │   └── chat_agent.py            # NEW: OpenAI agent implementation
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   ├── main.py
│   └── middleware.py
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Web application structure with separate frontend and backend. Addition of MCP server and AI agent modules to backend for natural language processing and secure tool-based task management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional AI/MCP modules | Specific requirement for AI-powered natural language interface | Traditional REST API would not meet feature requirements |