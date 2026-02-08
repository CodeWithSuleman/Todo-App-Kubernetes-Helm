---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **Core Authentication Flow**
   - User signup with validation
   - User signin with credential verification
   - Secure logout mechanism

2. **Password Security**
   - Hash passwords using strong algorithms (bcrypt/argon2)
   - Never store plain-text passwords
   - Apply proper salt rounds

3. **Token-Based Auth**
   - Generate JWT access tokens
   - Verify and decode tokens on protected routes
   - Handle token expiration and refresh logic

4. **Better Auth Integration**
   - Configure Better Auth provider
   - Use built-in session and token handling
   - Integrate with frontend and backend seamlessly

## Best Practices
- Always hash passwords before storing
- Use HTTPS for all auth requests
- Keep JWT secrets secure (env variables)
- Set short-lived access tokens
- Validate input to prevent injection attacks
- Follow least-privilege access control

## Example Structure

```ts
// Signup
POST /api/auth/signup
- Validate input
- Hash password
- Store user in database

// Signin
POST /api/auth/signin
- Verify credentials
- Generate JWT
- Return token

// Protected Route
GET /api/profile
- Verify JWT
- Return user data
