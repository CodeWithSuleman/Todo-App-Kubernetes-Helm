---
description: "Task list for AI Backend & MCP Tooling feature implementation"
---

# Tasks: AI Backend & MCP Tooling

**Input**: Design documents from `/specs/001-ai-backend-mcp-tooling/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install OpenAI and MCP SDK dependencies in backend/pyproject.toml
- [x] T002 [P] Create MCP module structure in backend/src/mcp/__init__.py
- [x] T003 [P] Create agents module structure in backend/src/agents/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Conversation model in backend/src/models/conversation.py
- [x] T005 Create Message model in backend/src/models/message.py
- [x] T006 [P] Update database.py to include new models in table creation
- [x] T007 [P] Create ConversationService in backend/src/services/conversation_service.py
- [x] T008 Setup JWT authentication validation for chat endpoint in backend/src/api/chat.py
- [x] T009 Create MCP server foundation in backend/src/mcp/server.py
- [x] T010 Configure CORS for chat endpoint in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with an AI assistant via chat interface to manage their todo tasks using natural language

**Independent Test**: Can be fully tested by sending natural language requests to the chat endpoint and verifying that the appropriate task operations are performed, delivering the ability for users to manage tasks via conversation.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Contract test for chat endpoint in backend/tests/contract/test_chat_api.py
- [ ] T012 [P] [US1] Integration test for natural language task creation in backend/tests/integration/test_natural_language_todo.py

### Implementation for User Story 1

- [x] T013 [P] [US1] Create add_task MCP tool in backend/src/mcp/tools.py
- [x] T014 [P] [US1] Create list_tasks MCP tool in backend/src/mcp/tools.py
- [x] T015 [P] [US1] Create update_task MCP tool in backend/src/mcp/tools.py
- [x] T016 [P] [US1] Create complete_task MCP tool in backend/src/mcp/tools.py
- [x] T017 [P] [US1] Create delete_task MCP tool in backend/src/mcp/tools.py
- [x] T018 [US1] Implement OpenAI agent with tool registration in backend/src/agents/chat_agent.py
- [x] T019 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/chat.py
- [x] T020 [US1] Add conversation persistence to chat endpoint
- [x] T021 [US1] Add tool call logging to chat responses

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Multi-User Access (Priority: P2)

**Goal**: Ensure users can only interact with their own tasks, with the system enforcing user isolation and preventing cross-user access to task data

**Independent Test**: Can be tested by authenticating as different users and verifying that each user can only access their own tasks, delivering secure multi-user isolation.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US2] Contract test for user isolation in backend/tests/contract/test_user_isolation.py
- [ ] T023 [P] [US2] Integration test for cross-user access prevention in backend/tests/integration/test_cross_user_access.py

### Implementation for User Story 2

- [x] T024 [P] [US2] Add user ownership validation to add_task MCP tool
- [x] T025 [P] [US2] Add user ownership validation to list_tasks MCP tool
- [x] T026 [P] [US2] Add user ownership validation to update_task MCP tool
- [x] T027 [P] [US2] Add user ownership validation to complete_task MCP tool
- [x] T028 [P] [US2] Add user ownership validation to delete_task MCP tool
- [x] T029 [US2] Implement 403 Forbidden response for unauthorized access
- [x] T030 [US2] Add route-level user_id validation against JWT in chat endpoint

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation Continuity (Priority: P3)

**Goal**: Allow users to resume a conversation with the AI assistant after disconnecting, maintaining context and history of previous interactions

**Independent Test**: Can be tested by creating a conversation, disconnecting, and reconnecting with the same conversation ID to verify continuity, delivering persistent conversation context.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US3] Contract test for conversation resume in backend/tests/contract/test_conversation_resume.py
- [ ] T032 [P] [US3] Integration test for conversation context reconstruction in backend/tests/integration/test_conversation_context.py

### Implementation for User Story 3

- [x] T033 [P] [US3] Implement conversation context reconstruction from database in chat_agent.py
- [x] T034 [US3] Add conversation history loading to chat endpoint
- [x] T035 [US3] Modify chat agent to include conversation history in AI requests
- [x] T036 [US3] Add conversation_id parameter handling to chat endpoint
- [x] T037 [US3] Update message persistence to include conversation context

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T038 [P] Documentation updates in docs/
- [ ] T039 Error handling for malformed natural language input
- [ ] T040 [P] Performance optimization for AI response times
- [ ] T041 [P] Additional unit tests in backend/tests/unit/
- [ ] T042 Security hardening for AI tool access
- [ ] T043 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 tools with added security
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 with conversation context

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all MCP tools for User Story 1 together:
Task: "Create add_task MCP tool in backend/src/mcp/tools.py"
Task: "Create list_tasks MCP tool in backend/src/mcp/tools.py"
Task: "Create update_task MCP tool in backend/src/mcp/tools.py"
Task: "Create complete_task MCP tool in backend/src/mcp/tools.py"
Task: "Create delete_task MCP tool in backend/src/mcp/tools.py"

# Launch agent and endpoint together:
Task: "Implement OpenAI agent with tool registration in backend/src/agents/chat_agent.py"
Task: "Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/chat.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence