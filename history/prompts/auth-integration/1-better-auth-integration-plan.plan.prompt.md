---
id: 1
title: Better Auth Integration Plan
stage: plan
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-integration
branch: 002-auth-security
user: user
command: "sp.plan auth-integration"
labels: ["auth", "integration", "jwt", "better-auth", "planning"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/auth-integration/plan.md"
tests:
  - "no tests yet"
---

## Prompt

Create a comprehensive plan for integrating Better Auth with the existing JWT system according to the implementation plan provided.

## Response snapshot

# Better Auth Integration Plan

## 1. Scope and Dependencies

### In Scope
- Integrate Better Auth token generation with existing JWT validation system
- Extend JWT token expiration from 30 minutes to 7 days (10080 minutes)
- Ensure compatibility between Better Auth tokens and existing backend middleware
- Maintain all existing authorization and user isolation mechanisms
- Add token refresh capability for extended sessions

### Out of Scope
- Implementing Better Auth in the frontend (frontend responsibility)
- Changing database schema or user models
- Modifying core business logic of todo operations
- Implementing OAuth providers or social login

### External Dependencies
- Better Auth library (frontend implementation responsibility)
- JWT secret key shared between frontend and backend
- Existing database and user isolation mechanisms

## 2. Key Decisions and Rationale

### JWT Algorithm and Secret Consistency
- **Decision**: Use HS256 algorithm with shared JWT_SECRET_KEY
- **Rationale**: Ensures compatibility between Better Auth tokens and existing validation system
- **Trade-offs**: Symmetric key approach vs asymmetric; simplicity over distributed key management

### Token Expiration Duration
- **Decision**: Set token expiration to 7 days (10080 minutes)
- **Rationale**: Balances security (shorter windows) with usability (longer sessions)
- **Trade-offs**: Increased exposure window vs improved user experience

### Token Refresh Mechanism
- **Decision**: Implement refresh endpoint to extend token validity
- **Rationale**: Allows extended sessions without requiring full re-authentication
- **Trade-offs**: Complexity increase vs improved user experience

### Principles
- Maintain backward compatibility with existing JWT validation
- Preserve existing user isolation and authorization mechanisms
- Minimal changes to existing codebase
- Reversible implementation approach

## 3. Interfaces and API Contracts

### New Authentication Endpoints
- `POST /api/v1/auth/refresh-token` - Refresh existing token
  - Input: Authorization header with existing token
  - Output: New token with extended expiration
  - Errors: 401 (invalid/expired token), 500 (server error)

- `GET /api/v1/auth/validate-token` - Validate existing token
  - Input: Authorization header with token
  - Output: User ID and token validity information
  - Errors: 401 (invalid token), 500 (server error)

### Modified Configuration
- `ACCESS_TOKEN_EXPIRE_MINUTES` in config.py: Updated from 30 to 10080
- JWT secret and algorithm remain unchanged for compatibility

### Versioning Strategy
- No breaking changes to existing API
- New endpoints follow existing v1 versioning
- Backward compatible with existing JWT tokens

### Error Taxonomy
- 401 Unauthorized: Invalid, expired, or missing token
- 500 Internal Server Error: Server-side token processing errors
- Standard error response format maintained

### 4. Non-Functional Requirements (NFRs) and Budgets

### Performance
- p95 token validation latency: < 50ms
- p95 token refresh latency: < 100ms
- No performance degradation to existing endpoints

### Reliability
- SLO: 99.9% successful token validation rate
- Graceful handling of token expiration and invalidation
- No impact on existing todo operations availability

### Security
- Token validation must be consistent with existing middleware
- User isolation preserved in all operations
- Secrets stored securely in environment variables
- No changes to existing authorization logic

### Cost
- No additional infrastructure costs
- Minimal computational overhead for extended tokens

## 5. Data Management and Migration

### Source of Truth
- JWT tokens remain stateless (no database storage)
- User identity derived from token claims
- Existing user_id in 'sub' claim maintained

### Schema Evolution
- No database schema changes required
- No migration scripts needed

### Data Retention
- No changes to existing data retention policies
- Token expiration handled by JWT standard

## 6. Operational Readiness

### Observability
- Log authentication events consistently with existing patterns
- Monitor token refresh and validation success rates
- Track error patterns in auth endpoints

### Alerting
- Alert on high error rates in auth endpoints
- Monitor for unexpected token validation failures

### Runbooks
- Document token refresh flow for operations
- Include troubleshooting steps for auth integration issues

### Deployment Strategy
- Deploy auth endpoints without downtime
- Gradual rollout of 7-day expiration (existing tokens unaffected until renewal)

### Feature Flags
- No feature flags needed (backward compatible changes)

## 7. Risk Analysis and Mitigation

### Risk 1: Token Compatibility Issues
- **Impact**: Better Auth tokens not accepted by existing middleware
- **Mitigation**: Thorough testing of token format compatibility
- **Blast Radius**: Authentication failures across all endpoints
- **Guardrail**: Maintain existing token validation for fallback

### Risk 2: Extended Token Exposure Window
- **Impact**: Longer-lived tokens increase potential security exposure
- **Mitigation**: Implement token refresh with revocation capability
- **Blast Radius**: Individual user accounts if tokens compromised
- **Guardrail**: Monitor for suspicious activity patterns

### Risk 3: User Isolation Breakdown
- **Impact**: Cross-user data access if token validation fails
- **Mitigation**: Comprehensive testing of authorization enforcement
- **Blast Radius**: Data integrity across user accounts
- **Guardrail**: Existing service-layer user_id validation

## 8. Evaluation and Validation

### Definition of Done
- [ ] JWT expiration updated to 7 days (10080 minutes)
- [ ] New auth endpoints implemented and documented
- [ ] Token refresh functionality working
- [ ] Better Auth compatible tokens validated successfully
- [ ] All existing endpoints continue to work with new tokens
- [ ] User isolation preserved and tested
- [ ] Error handling consistent with existing patterns

### Output Validation
- [ ] Token validation accepts Better Auth format tokens
- [ ] Token refresh extends validity correctly
- [ ] All todo endpoints properly authenticate new tokens
- [ ] Authorization checks prevent cross-user access
- [ ] Error responses follow existing format

### Testing Requirements
- [ ] Unit tests for token creation and validation functions
- [ ] Integration tests for auth endpoints
- [ ] End-to-end tests with Better Auth compatible tokens
- [ ] Security tests for user isolation

## 9. Architectural Decision Records (ADRs)

### ADR-001: JWT Algorithm Consistency for Better Auth Integration
- **Context**: Need to ensure tokens generated by Better Auth are compatible with existing backend validation
- **Decision**: Use HS256 algorithm with shared JWT_SECRET_KEY
- **Status**: Implemented
- **Consequences**: Simplifies integration but requires shared secret management

### ADR-002: 7-Day Token Expiration Duration
- **Context**: Balance between security and usability for authentication tokens
- **Decision**: Set ACCESS_TOKEN_EXPIRE_MINUTES to 10080 (7 days)
- **Status**: Implemented
- **Consequences**: Improved user experience with longer sessions, increased exposure window

## Outcome

- ✅ Impact: Created comprehensive plan for Better Auth integration with existing JWT system
- 🧪 Tests: no tests yet
- 📁 Files: specs/auth-integration/plan.md
- 🔁 Next prompts: Will create spec and tasks based on this plan
- 🧠 Reflection: Plan covers all aspects of integration while maintaining compatibility

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A