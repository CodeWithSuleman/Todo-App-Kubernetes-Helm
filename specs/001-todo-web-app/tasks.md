---
description: "Task list for Backend + Database Foundation implementation"
---

# Tasks: Backend + Database Foundation

**Input**: Design documents from `/specs/001-todo-web-app/`

**Prerequisites**: plan.md (required), spec.md (required for requirements), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are organized by implementation phases to enable systematic development of the backend foundation.

## Format: `[ID] [P?] [Foundation] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Foundation]**: Backend foundation specific tasks
- Include exact file paths in descriptions

## Path Conventions

- **Backend app**: `backend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Backend project initialization and basic structure

- [X] T001 Create project structure with backend/ directory only
- [X] T002 Initialize Python project with FastAPI, SQLModel, Neon dependencies in backend/
- [X] T003 [P] Configure linting and formatting tools for Python (black, flake8, mypy)
- [X] T004 Configure environment configuration management for backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend infrastructure that MUST be complete before frontend integration

**⚠️ CRITICAL**: No frontend integration can begin until this phase is complete

- [X] T005 Setup database schema and migrations framework with SQLModel
- [X] T006 Setup API routing and middleware structure in FastAPI backend
- [X] T007 Create Todo model in backend/src/models/todo.py (no User model)
- [X] T008 Configure error handling and logging infrastructure in backend
- [X] T009 Setup database connection with Neon PostgreSQL
- [X] T010 Implement JWT token verification middleware in FastAPI (extract user_id from 'sub' field)
- [X] T011 Create API endpoints for todos without authentication flows
- [X] T012 Implement user_id filtering in all database queries for data isolation

**Checkpoint**: Backend Foundation ready - frontend integration can now begin in Spec-2

---

## Phase 3: Todo Management Foundation (Priority: P1) 🎯 MVP

**Goal**: Enable JWT-authenticated users to create, read, update, and delete their personal todo items with proper user isolation

**Independent Test**: Create, view, update, and delete todo items with proper JWT verification and user isolation

### Tests for Todo Management (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [Foundation] Contract test for /api/v1/todos GET endpoint in backend/tests/contract/test_todos_get.py
- [ ] T014 [P] [Foundation] Contract test for /api/v1/todos POST endpoint in backend/tests/contract/test_todos_create.py
- [ ] T015 [P] [Foundation] Contract test for /api/v1/todos/{todo_id} PUT endpoint in backend/tests/contract/test_todos_update.py
- [ ] T016 [P] [Foundation] Contract test for /api/v1/todos/{todo_id} DELETE endpoint in backend/tests/contract/test_todos_delete.py
- [ ] T017 [P] [Foundation] Contract test for /api/v1/todos/{todo_id}/toggle-complete PATCH endpoint in backend/tests/contract/test_todos_toggle.py

### Implementation for Todo Management Foundation

- [X] T018 [P] [Foundation] Create Todo model in backend/src/models/todo.py (UUID id, user_id from JWT)
- [X] T019 [Foundation] Implement Todo service with CRUD operations in backend/src/services/todo_service.py
- [X] T020 [Foundation] Implement /api/v1/todos GET endpoint in backend/src/api/todos.py
- [X] T021 [Foundation] Implement /api/v1/todos POST endpoint in backend/src/api/todos.py
- [X] T022 [Foundation] Implement /api/v1/todos/{todo_id} GET endpoint in backend/src/api/todos.py
- [X] T023 [Foundation] Implement /api/v1/todos/{todo_id} PUT endpoint in backend/src/api/todos.py
- [X] T024 [Foundation] Implement /api/v1/todos/{todo_id} DELETE endpoint in backend/src/api/todos.py
- [X] T025 [Foundation] Implement /api/v1/todos/{todo_id}/toggle-complete PATCH endpoint in backend/src/api/todos.py
- [X] T026 [Foundation] Add JWT verification and user_id filtering to ensure users can only access their own todos

**Checkpoint**: At this point, Todo Management should be fully functional and testable with JWT verification

---

## Phase 4: Backend Optimization & Documentation (Priority: P2)

**Goal**: Optimize backend performance and prepare for frontend integration in Spec-2

**Independent Test**: Verify backend performance and documentation completeness

### Implementation for Backend Optimization

- [X] T027 [P] [Foundation] Optimize database queries for performance in backend/src/services/todo_service.py
- [X] T028 [Foundation] Add database indexes for efficient user todo retrieval
- [X] T029 [Foundation] Implement proper database transaction handling for data integrity
- [X] T030 [Foundation] Add comprehensive error handling and user-friendly error messages
- [X] T031 [Foundation] Add comprehensive logging for debugging and monitoring
- [X] T032 [Foundation] Create documentation files (spec.md, plan.md, data-model.md, quickstart.md)
- [X] T033 [Foundation] Run quickstart.md validation to ensure deployment works

**Checkpoint**: Backend Foundation is complete and ready for frontend integration

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [X] T034 [P] Documentation updates in specs/001-todo-web-app/
- [X] T035 Code cleanup and refactoring across all backend modules
- [ ] T036 Performance optimization across all endpoints
- [ ] T037 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T038 Security hardening (rate limiting, input validation, etc.)
- [X] T039 Validate all environment configurations and .env files
- [X] T040 Final validation of JWT verification and user data isolation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all other work
- **Todo Management (Phase 3)**: Depends on Foundational phase completion
- **Optimization (Phase 4)**: Depends on Todo Management completion
- **Polish (Final Phase)**: Depends on all previous phases being complete

### Within Each Phase

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before optimization

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests for a phase marked [P] can run in parallel
- Models within a phase marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (Backend Foundation Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all other work)
3. Complete Phase 3: Todo Management Foundation
4. Complete Phase 4: Backend Optimization & Documentation
5. Complete Phase 5: Polish and validation
6. **STOP and VALIDATE**: Backend is ready for frontend integration in Spec-2

### Validation Points

1. Complete Setup + Foundational → Foundation ready for testing
2. Add Todo Management → Test with JWT tokens → Validate data isolation
3. Add Optimization → Test performance → Validate documentation
4. Complete Polish → Final validation → Ready for Spec-2 integration

---

## Notes

- [P] tasks = different files, no dependencies
- [Foundation] label indicates backend foundation specific tasks
- Each phase should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate phase independently
- Avoid: vague tasks, same file conflicts, dependencies that break independence