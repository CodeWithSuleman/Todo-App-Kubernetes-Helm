# Research: AI Backend & MCP Tooling

**Feature**: AI Backend & MCP Tooling
**Date**: 2026-02-05

## Overview

This research document addresses the technical requirements for implementing a stateless AI-powered backend that enables natural-language todo management using OpenAI Agents SDK and MCP (Model Context Protocol).

## Technology Research

### OpenAI Agents SDK

**Decision**: Use OpenAI Assistant API for the AI agent functionality
**Rationale**: The OpenAI Assistant API provides a managed way to create AI agents that can use tools/functions. It's well-documented and integrates well with the existing Python backend.
**Alternatives considered**:
- LangChain agents: More complex setup but more flexible
- Custom OpenAI function calling: Requires more manual implementation

### MCP (Model Context Protocol) SDK

**Decision**: Implement MCP server using the official Python SDK
**Rationale**: MCP is designed for connecting AI models to tools and resources. It provides a standardized way to expose backend functionality to AI agents.
**Alternatives considered**:
- Direct function calling: Less standardized, harder to maintain
- REST API with AI parsing: Doesn't leverage MCP benefits

### Conversation and Message Models

**Decision**: Extend existing SQLModel-based data models to include Conversation and Message entities
**Rationale**: Maintains consistency with existing tech stack while fulfilling persistence requirements
**Alternatives considered**:
- Separate database: Would violate separation of concerns principle
- In-memory storage: Would violate statelessness requirement

### Authentication and Authorization

**Decision**: Leverage existing JWT-based authentication system with route-level validation
**Rationale**: The existing Better Auth integration provides JWT tokens that can be validated at the route level to ensure user identity
**Implementation**: Extract user_id from JWT and validate against route parameter

### MCP Tool Definitions

**Decision**: Create 5 specific MCP tools matching the required functionality: add_task, list_tasks, update_task, complete_task, delete_task
**Rationale**: These directly correspond to the functional requirements in the specification
**Schema**: Each tool will follow strict input/output schemas to ensure deterministic behavior

## Architecture Decisions

### Stateless Operation

**Decision**: Reconstruct conversation context from database on each request
**Rationale**: Ensures the server remains stateless between requests as required by the specification and constitution
**Implementation**: Load conversation history from database at the beginning of each chat request

### Tool Enforcement

**Decision**: All state changes must occur through MCP tools, not direct database access
**Rationale**: Ensures compliance with the specification requirement that "Agent must not directly access the database"
**Implementation**: MCP tools will handle all database operations with proper user scoping

## Security Considerations

### User Isolation

**Decision**: Enforce user ownership in all MCP tools
**Rationale**: Critical for preventing cross-user access to tasks
**Implementation**: Each MCP tool will validate that the user owns the resources they're accessing

### JWT Validation

**Decision**: Validate JWT tokens at the chat endpoint level
**Rationale**: Ensures authentication before processing any natural language requests
**Implementation**: Dependency injection for JWT validation in the chat endpoint

## Data Model Extensions

### Conversation Model
- user_id: UUID (foreign key to user)
- id: UUID (primary key)
- created_at: datetime
- updated_at: datetime

### Message Model
- user_id: UUID (foreign key to user)
- conversation_id: UUID (foreign key to conversation)
- id: UUID (primary key)
- role: str (user/assistant/system)
- content: str
- created_at: datetime
- updated_at: datetime

These models align with the existing SQLModel patterns in the codebase while fulfilling the persistence requirements.

## Implementation Strategy

### Phase 1: Infrastructure
1. Add Conversation and Message models
2. Create MCP server infrastructure
3. Define MCP tool schemas

### Phase 2: Integration
1. Connect OpenAI agent to MCP tools
2. Implement chat endpoint with authentication
3. Add conversation persistence

### Phase 3: Validation
1. Test tool accuracy and security
2. Verify statelessness
3. Confirm restart safety