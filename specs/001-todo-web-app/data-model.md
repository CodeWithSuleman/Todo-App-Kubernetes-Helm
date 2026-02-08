# Data Model for Backend + Database Foundation

## Todo Entity
- **id** (UUID/string): Primary identifier (UUID-based)
- **title** (string): Task title (required, max 255 chars)
- **description** (text): Optional detailed description
- **completed** (boolean): Completion status (default: false)
- **user_id** (string): User identifier extracted from JWT 'sub' field (no foreign key to users table)
- **created_at** (datetime): Timestamp of task creation
- **updated_at** (datetime): Timestamp of last update

## Relationships
- No relationships to User entity (removed in scope correction)
- **Data Isolation**: All queries must filter by user_id field for proper user isolation

## Validation Rules
- Title must be 1-255 characters
- User_id must be present and valid string from JWT
- Only the owning user (based on JWT user_id) can modify/delete a todo

## State Transitions
- **Todo.completed**: Can transition from false to true (mark complete) or true to false (mark incomplete)