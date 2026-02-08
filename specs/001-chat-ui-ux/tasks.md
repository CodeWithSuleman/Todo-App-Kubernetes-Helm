# Implementation Tasks: Chat Interface & AI UX

## Feature Overview
Implementation of a clean, responsive chat UI for interacting with the AI todo assistant. The feature provides an auth-aware chat interface that integrates with the existing `/api/{user_id}/chat` endpoint to allow users to manage their todos using natural language.

**Branch**: `001-chat-ui-ux` | **Date**: 2026-02-05 | **Spec**: [link to spec](./spec.md)

## Dependencies
- Backend `/api/v1/{user_id}/chat` endpoint is operational
- JWT authentication system is integrated with Better Auth
- User session management is working

## Parallel Execution Examples
- T010-T015 can be executed in parallel after T005
- T020-T025 can be executed in parallel after foundational setup
- User Story 1 components can be developed independently from User Story 2 components

## Implementation Strategy
1. Start with MVP: Basic chat UI that can send/receive messages from API (User Story 1)
2. Add conversation persistence (User Story 2)
3. Enhance with loading/error states (User Story 3)
4. Polish with animations, accessibility, and edge case handling

---

## Phase 1: Setup Tasks

### Goal
Prepare the development environment and project structure for chat interface implementation.

- [x] T001 Create protected chat page directory in frontend: `frontend/app/protected/chat`
- [x] T002 Create chat components directory: `frontend/components/chat`
- [x] T003 Create chat services directory: `frontend/lib/api/chat`
- [x] T004 Set up TypeScript types for chat entities in `frontend/lib/types/chat.ts`
- [x] T005 Review existing auth context to ensure compatibility with chat routes

---

## Phase 2: Foundational Tasks

### Goal
Implement core components and services required by all user stories.

- [x] T010 [P] Create ChatMessage type definition in `frontend/lib/types/chat.ts`
- [x] T011 [P] Create Conversation type definition in `frontend/lib/types/chat.ts`
- [x] T012 [P] Create ChatState type definition in `frontend/lib/types/chat.ts`
- [x] T013 [P] Create ChatRequest/ChatResponse type definitions in `frontend/lib/types/chat.ts`
- [x] T014 Create utility functions for timestamp formatting in `frontend/lib/utils/time.ts`
- [x] T015 Create utility functions for message sanitization in `frontend/lib/utils/sanitize.ts`
- [x] T016 [P] Create shared constants for chat functionality in `frontend/lib/constants/chat.ts`

---

## Phase 3: User Story 1 - Chat with AI Assistant for Todo Management (Priority: P1)

### Goal
Enable logged-in users to interact with an AI assistant to manage their todos using natural language.

### Independent Test
The user can type a natural language request like "Add a new task to buy groceries" and see a new todo appear in their list, or ask "What are my tasks for today?" and see their relevant tasks listed.

### Tasks
- [x] T020 [US1] Create ChatService to handle API communication with `/api/v1/{user_id}/chat` in `frontend/lib/api/chat/service.ts`
- [x] T021 [US1] Implement JWT authentication headers for chat API calls in ChatService
- [x] T022 [US1] Create MessageInput component in `frontend/components/chat/MessageInput.tsx`
- [x] T023 [US1] Create MessageBubble component to display chat messages in `frontend/components/chat/MessageBubble.tsx`
- [x] T024 [US1] Create MessageList component to display conversation history in `frontend/components/chat/MessageList.tsx`
- [x] T025 [US1] Create ChatContainer component to manage chat UI state in `frontend/components/chat/ChatContainer.tsx`
- [x] T026 [US1] Implement message sending functionality with proper error handling
- [x] T027 [US1] Implement message receiving and display logic
- [x] T028 [US1] Create basic chat page in `frontend/app/protected/chat/page.tsx`
- [x] T029 [US1] Integrate ChatContainer with the chat page
- [x] T030 [US1] Test end-to-end chat functionality with AI assistant

---

## Phase 4: User Story 2 - Resume Conversations Across Sessions (Priority: P2)

### Goal
Allow users to return to previous conversations and continue where they left off, with conversation context preserved across browser refreshes.

### Independent Test
After closing the browser and returning, the user can see their previous conversation history and continue interacting with the AI where they left off.

### Tasks
- [x] T040 [US2] Create ConversationStorage service for localStorage management in `frontend/lib/api/chat/storage.ts`
- [x] T041 [US2] Implement saveConversation function to persist conversation to localStorage
- [x] T042 [US2] Implement loadConversations function to retrieve conversations from localStorage
- [x] T043 [US2] Implement deleteConversation function to remove conversations from localStorage
- [x] T044 [US2] Add conversation persistence to ChatService when messages are exchanged
- [x] T045 [US2] Create ConversationHistory component to display past conversations in `frontend/components/chat/ConversationHistory.tsx`
- [x] T046 [US2] Implement conversation switching functionality
- [x] T047 [US2] Add auto-load of most recent conversation on page load
- [x] T048 [US2] Implement conversation metadata (last message, timestamp) in storage
- [ ] T049 [US2] Test conversation persistence across browser refreshes
- [ ] T050 [US2] Test conversation resumption across different browser sessions

---

## Phase 5: User Story 3 - Handle Loading, Error, and Empty States (Priority: P3)

### Goal
Provide appropriate UI feedback for loading states, errors, and empty states in the chat interface.

### Independent Test
During API calls, users see loading indicators; when errors occur, users see clear error messages; when no conversations exist, users see helpful empty state guidance.

### Tasks
- [x] T060 [US3] Create LoadingIndicator component in `frontend/components/chat/LoadingIndicator.tsx`
- [x] T061 [US3] Create ErrorMessage component in `frontend/components/chat/ErrorMessage.tsx`
- [x] T062 [US3] Create EmptyState component for initial chat view in `frontend/components/chat/EmptyState.tsx`
- [x] T063 [US3] Integrate loading indicators with message sending/receiving in ChatContainer
- [x] T064 [US3] Implement error state handling for API failures in ChatService
- [x] T065 [US3] Display appropriate error messages for different failure scenarios
- [x] T066 [US3] Implement retry mechanism for failed API calls
- [x] T067 [US3] Add visual feedback for "sending" status of user messages
- [x] T068 [US3] Create error boundary for chat components
- [ ] T069 [US3] Test loading state display during API calls
- [ ] T070 [US3] Test error state display for various failure scenarios

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Enhance the user experience with additional features, accessibility improvements, and error handling.

### Tasks
- [x] T080 Add keyboard accessibility to chat interface (Enter to send, arrow keys for history)
- [x] T081 Implement auto-scroll to bottom when new messages arrive
- [x] T082 Add message timestamps to MessageBubble component
- [ ] T083 Implement message input history (up/down arrows to navigate previous messages)
- [x] T084 Add character limits to message input with visual feedback
- [x] T085 Implement proper XSS prevention for message content display
- [x] T086 Add smooth animations for message appearance/disappearance
- [x] T087 Create responsive design for mobile chat experience
- [x] T088 Add proper focus management for accessibility
- [ ] T089 Implement auto-reconnection when JWT token expires during chat
- [ ] T090 Conduct end-to-end testing of all user stories together
- [ ] T091 Document chat API integration for future developers
- [ ] T092 Add unit tests for ChatService and utility functions