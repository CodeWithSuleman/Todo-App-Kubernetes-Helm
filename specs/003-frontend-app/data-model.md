# Data Model: Frontend Application & User Experience

## 1. Core Entities

### 1.1 User Entity
- **Name**: User
- **Fields**:
  - id: string (unique identifier from auth system)
  - email: string (user's email address)
  - name: string (optional, user's display name)
  - createdAt: Date (when user account was created)
  - updatedAt: Date (when user account was last updated)
- **Validation**:
  - email: must be valid email format
  - id: required, unique
- **Relationships**: Owns multiple Tasks

### 1.2 Task Entity
- **Name**: Task
- **Fields**:
  - id: string (unique identifier)
  - title: string (task title, max 255 chars)
  - description: string (optional, task description)
  - completed: boolean (completion status)
  - userId: string (foreign key to User)
  - createdAt: Date (when task was created)
  - updatedAt: Date (when task was last updated)
  - priority: string (optional, enum: low, medium, high)
  - dueDate: Date (optional, deadline for task)
- **Validation**:
  - title: required, max 255 characters
  - userId: required, must reference valid user
  - completed: boolean, defaults to false
  - priority: optional, must be one of allowed values
- **Relationships**: Belongs to one User

## 2. Authentication-Related Entities

### 2.1 Session Entity
- **Name**: Session
- **Fields**:
  - token: string (JWT token)
  - userId: string (associated user ID)
  - expiresAt: Date (expiration timestamp)
  - createdAt: Date (session creation time)
- **Validation**:
  - token: required, valid JWT format
  - userId: required, must reference valid user
  - expiresAt: required, future date
- **State Transitions**:
  - Active → Expired (when expiresAt is reached)
  - Active → Revoked (on logout)

### 2.2 API Response Structures

#### 2.2.1 Auth Response
- **Structure**: AuthResponse
- **Fields**:
  - user: User (authenticated user object)
  - token: string (JWT token)
  - expiresIn: number (seconds until expiration)

#### 2.2.2 Task Response
- **Structure**: TaskResponse
- **Fields**:
  - data: Task | Task[] (single task or array of tasks)
  - message?: string (optional success/error message)
  - error?: string (optional error details)

#### 2.2.3 Error Response
- **Structure**: ErrorResponse
- **Fields**:
  - error: string (error message)
  - code: string (error code)
  - details?: object (optional error details)

## 3. Component State Models

### 3.1 Form State Models

#### 3.1.1 LoginForm State
- **Structure**: LoginFormState
- **Fields**:
  - email: string (user email input)
  - password: string (user password input)
  - loading: boolean (form submission status)
  - error: string (form error message)

#### 3.1.2 SignupForm State
- **Structure**: SignupFormState
- **Fields**:
  - name: string (user name input)
  - email: string (user email input)
  - password: string (user password input)
  - confirmPassword: string (password confirmation)
  - loading: boolean (form submission status)
  - error: string (form error message)

#### 3.1.3 TaskForm State
- **Structure**: TaskFormState
- **Fields**:
  - title: string (task title input)
  - description: string (task description input)
  - priority: string (task priority)
  - dueDate: string (due date input)
  - loading: boolean (form submission status)
  - error: string (form error message)

### 3.2 UI State Models

#### 3.2.1 TaskList State
- **Structure**: TaskListState
- **Fields**:
  - tasks: Task[] (list of tasks)
  - loading: boolean (data loading status)
  - error: string (error message if any)
  - filter: string (filter criteria: all, active, completed)
  - sort: string (sort criteria: date, priority)

#### 3.2.2 Toast State
- **Structure**: ToastState
- **Fields**:
  - id: string (unique toast identifier)
  - message: string (toast message)
  - type: string (success, error, warning, info)
  - duration: number (display duration in ms)

## 4. API Request/Response Models

### 4.1 Task API Models

#### 4.1.1 Create Task Request
- **Structure**: CreateTaskRequest
- **Fields**:
  - title: string (required)
  - description?: string (optional)
  - priority?: string (optional, default: medium)
  - dueDate?: string (optional)

#### 4.1.2 Update Task Request
- **Structure**: UpdateTaskRequest
- **Fields**:
  - title?: string (optional)
  - description?: string (optional)
  - completed?: boolean (optional)
  - priority?: string (optional)
  - dueDate?: string (optional)

#### 4.1.3 Task List Response
- **Structure**: TaskListResponse
- **Fields**:
  - tasks: Task[] (array of user's tasks)
  - total: number (total number of tasks)
  - page: number (current page number)
  - limit: number (number of tasks per page)

## 5. Validation Rules

### 5.1 Task Validation
- Title length: 1-255 characters
- Description length: 0-1000 characters
- Priority values: "low", "medium", "high"
- Due date: must be a valid date format

### 5.2 User Validation
- Email format: must be valid email address
- Password strength: minimum 8 characters with at least one uppercase, lowercase, number, and symbol

### 5.3 Authentication Validation
- JWT format: must be a valid JWT token
- Token expiration: must not be expired
- User ID: must exist in the system