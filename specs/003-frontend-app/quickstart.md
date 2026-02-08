# Quickstart Guide: Frontend Application & User Experience

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git version control
- Access to backend API endpoints

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_COOKIE_NAME=auth_token
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting
- `npm run test` - Run unit tests

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages (login, signup)
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   └── layout.tsx
│   ├── (protected)/       # Protected pages (dashboard, tasks)
│   │   ├── dashboard/page.tsx
│   │   ├── tasks/page.tsx
│   │   ├── tasks/[id]/page.tsx
│   │   └── layout.tsx
│   ├── globals.css        # Global styles
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── auth/             # Authentication components
│   ├── tasks/            # Task management components
│   ├── ui/               # Base UI components (buttons, inputs, etc.)
│   └── providers/        # Context providers
├── lib/                  # Utility functions and services
│   ├── auth/             # Authentication utilities
│   ├── api/              # API client and services
│   └── types/            # TypeScript type definitions
├── public/               # Static assets
└── next.config.js        # Next.js configuration
```

## Development Workflow

### 1. Creating New Pages
Use the App Router convention:
```
app/new-feature/page.tsx
```

### 2. Adding New Components
Place reusable components in the `components/` directory:
```
components/ui/button.tsx
components/auth/login-form.tsx
```

### 3. API Integration
All API calls should go through the centralized service in `lib/api/`:
```typescript
import { apiClient } from '@/lib/api/client'

const tasks = await apiClient.get('/tasks')
```

### 4. Authentication
Protected routes automatically check for valid sessions:
```typescript
// This component will redirect unauthenticated users to login
import { useAuth } from '@/components/providers/auth-provider'

function ProtectedPage() {
  const { user, isLoading } = useAuth()

  if (isLoading) return <div>Loading...</div>
  if (!user) return <div>Please log in</div>

  return <div>Protected content</div>
}
```

## Key Technologies

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **HTTP Client**: Custom fetch wrapper with interceptors
- **State Management**: React Context API + Hooks
- **Testing**: Jest, React Testing Library, Cypress

## Common Tasks

### Adding a New Task Feature
1. Create the UI component in `components/tasks/`
2. Add API methods in `lib/api/tasks.ts`
3. Create the page in `app/(protected)/tasks/`
4. Implement the business logic

### Adding Authentication to a Page
1. Wrap the page with `AuthProvider`
2. Use the `useAuth` hook to check authentication status
3. Implement appropriate loading/error states

### Adding New API Endpoints
1. Add the method to the appropriate service in `lib/api/`
2. Ensure JWT token is included in the request
3. Handle potential 401 responses appropriately