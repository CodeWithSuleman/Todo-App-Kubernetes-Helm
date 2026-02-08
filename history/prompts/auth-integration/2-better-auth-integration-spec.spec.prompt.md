---
id: 2
title: Better Auth Integration Spec
stage: spec
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-integration
branch: 002-auth-security
user: user
command: "sp.specify auth-integration"
labels: ["auth", "integration", "jwt", "better-auth", "specification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/auth-integration/spec.md"
tests:
  - "no tests yet"
---

## Prompt

Create a comprehensive specification for integrating Better Auth with the existing JWT system based on the implementation plan.

## Response snapshot

# Better Auth Integration Specification

## Feature: Better Auth Integration with Existing JWT System

### User Story 1 (P1 - Critical)
As a developer, I want to extend the JWT token expiration from 30 minutes to 7 days so that users have longer-lasting sessions with Better Auth integration.

**Acceptance Criteria:**
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES in config.py is updated from 30 to 10080 (7 days)
- [ ] Existing JWT validation continues to work with new expiration time
- [ ] Token creation uses the new expiration duration

### User Story 2 (P1 - Critical)
As a system, I want to ensure Better Auth generated tokens are compatible with existing JWT validation middleware so that frontend and backend use the same authentication system.

**Acceptance Criteria:**
- [ ] Middleware can validate tokens generated with Better Auth compatible format
- [ ] Token payload structure (especially 'sub' claim for user_id) remains consistent
- [ ] Algorithm (HS256) and secret key remain compatible between systems

### User Story 3 (P2 - Important)
As an API consumer, I want to have authentication endpoints available so that I can manage token lifecycle including validation and refresh.

**Acceptance Criteria:**
- [ ] `/api/v1/auth/validate-token` endpoint exists and validates tokens
- [ ] `/api/v1/auth/refresh-token` endpoint exists and creates new tokens
- [ ] Both endpoints follow existing API patterns and error handling

### User Story 4 (P2 - Important)
As a security system, I want to maintain existing user isolation mechanisms so that users can only access their own data even with Better Auth tokens.

**Acceptance Criteria:**
- [ ] All existing todo endpoints continue to validate user ownership
- [ ] Service layer continues to filter by authenticated user_id
- [ ] Cross-user access prevention works with Better Auth tokens

### User Story 5 (P3 - Nice to Have)
As a developer, I want comprehensive documentation for the authentication integration so that frontend developers can properly implement Better Auth.

**Acceptance Criteria:**
- [ ] AUTH_INTEGRATION.md documents the integration approach
- [ ] API endpoints are documented with usage examples
- [ ] Configuration requirements for frontend are clearly specified

## Outcome

- ✅ Impact: Created comprehensive specification for Better Auth integration with acceptance criteria
- 🧪 Tests: no tests yet
- 📁 Files: specs/auth-integration/spec.md
- 🔁 Next prompts: Will create tasks based on this spec
- 🧠 Reflection: Spec defines clear user stories with prioritized acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A