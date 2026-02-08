# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

**Frontend**: Next.js 16+ (App Router)
**Backend**: Python FastAPI
**ORM**: SQLModel
**Database**: Neon Serverless PostgreSQL
**Authentication**: Better Auth (JWT-based)
**Testing**: [e.g., pytest, Jest, Cypress or NEEDS CLARIFICATION]
**Target Platform**: Web
**Performance Goals**: [domain-specific, e.g., <200ms p95 response time, or NEEDS CLARIFICATION]
**Constraints**: [e.g., Adherence to REST API contract, Stateless authentication]
**Scale/Scope**: [domain-specific, e.g., 10k users, or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] **Specification-driven**: Does this plan directly map to a `spec.md`?
- [ ] **Security-first**: Does the plan include JWT authentication for all protected routes?
- [ ] **Separation of Concerns**: Is there a clear boundary between frontend, backend, and data layers?
- [ ] **Reproducible Agent Execution**: Is the plan detailed enough for an agent to execute without ambiguity?
- [ ] **Production-ready**: Does the plan avoid demo-only shortcuts?
- [ ] **Traceable**: Are all features traceable to written specifications?
- [ ] **Strict REST API**: Does the plan adhere to the defined API endpoints and HTTP semantics?
- [ ] **Enforced Authentication**: Is authentication enforced on every protected route?
- [ ] **User Data Isolation**: Is user data isolation guaranteed at the API and database level?
- [ ] **Declared Tech Stack**: Does the plan only use the approved tech stack (Next.js, FastAPI, SQLModel, Neon, Better Auth)?

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
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Web application structure with separate frontend and backend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Additional framework] | [current need] | [why approved stack is insufficient] |
| [e.g., Stateful authentication] | [specific problem] | [why stateless is insufficient] |