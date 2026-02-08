# Quickstart Guide: Visual Design, UI Polish & Motion

## Setup Instructions

### Prerequisites
- Node.js 18+ installed
- Next.js 16+ project structure
- Framer Motion library installed
- CSS Modules or styled-jsx configured

### Installation Steps

1. **Install required dependencies**:
   ```bash
   npm install framer-motion
   ```

2. **Add theme provider to your app**:
   ```jsx
   // Wrap your application with the theme provider
   import { ThemeProvider } from '@/components/theme/theme-provider';

   export default function App({ Component, pageProps }) {
     return (
       <ThemeProvider>
         <Component {...pageProps} />
       </ThemeProvider>
     );
   }
   ```

3. **Configure design tokens** in your global styles:
   ```css
   /* globals.css */
   :root {
     /* Color tokens */
     --color-primary-start: 123 31 162; /* Purple 500 in RGB */
     --color-primary-end: 192 13 132;   /* Pink 600 in RGB */

     /* Spacing tokens */
     --spacing-xs: 0.25rem;
     --spacing-sm: 0.5rem;
     --spacing-md: 1rem;
     --spacing-lg: 1.5rem;
     --spacing-xl: 2rem;

     /* Animation tokens */
     --transition-normal: 300ms ease-out;
   }
   ```

4. **Import global styles** in your layout:
   ```jsx
   import '@/styles/globals.css';
   ```

## Usage Examples

### Using the Gradient Button Component
```jsx
import { GradientButton } from '@/components/ui/gradient-button';

export default function MyPage() {
  return (
    <GradientButton
      variant="primary"
      onClick={() => console.log('Clicked')}
    >
      Click Me
    </GradientButton>
  );
}
```

### Applying Animations to Components
```jsx
import { motion } from 'framer-motion';

export default function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="card"
    >
      Content goes here
    </motion.div>
  );
}
```

### Using Design Tokens in Components
```jsx
const MyComponent = () => {
  const styles = {
    padding: 'var(--spacing-lg)',
    borderRadius: 'var(--radius-md)',
    background: 'linear-gradient(to right, var(--color-primary-start), var(--color-primary-end))'
  };

  return <div style={styles}>Styled content</div>;
};
```

## Development Commands

### Running the Application
```bash
npm run dev
```

### Running Tests
```bash
npm run test
```

### Building for Production
```bash
npm run build
```

## Key Files to Modify

- `frontend/src/styles/globals.css` - Global design tokens
- `frontend/src/components/theme/theme-provider.jsx` - Theme provider component
- `frontend/src/components/ui/` - Reusable UI components with visual polish
- `frontend/src/components/animations/` - Animation components and hooks
- `frontend/app/layout.tsx` - Root layout with theme provider