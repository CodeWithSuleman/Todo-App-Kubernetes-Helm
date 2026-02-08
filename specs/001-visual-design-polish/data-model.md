# Data Model: Visual Design, UI Polish & Motion

## Design Tokens

### Color Tokens
- **primary-gradient**: Linear gradient from primary-500 to primary-600
- **secondary-gradient**: Linear gradient from secondary-500 to secondary-600
- **accent-gradient**: Linear gradient from accent-500 to accent-600
- **neutral-dark**: Dark background colors (gray-900, gray-800, etc.)
- **neutral-light**: Light text/ui colors (white, gray-100, etc.)

### Spacing Tokens
- **spacing-xs**: 0.25rem (4px)
- **spacing-sm**: 0.5rem (8px)
- **spacing-md**: 1rem (16px)
- **spacing-lg**: 1.5rem (24px)
- **spacing-xl**: 2rem (32px)
- **spacing-2xl**: 3rem (48px)

### Typography Tokens
- **font-family-primary**: Main font family for headings and body
- **font-size-xs**: 0.75rem (12px)
- **font-size-sm**: 0.875rem (14px)
- **font-size-base**: 1rem (16px)
- **font-size-lg**: 1.125rem (18px)
- **font-size-xl**: 1.25rem (20px)
- **font-size-2xl**: 1.5rem (24px)
- **font-size-3xl**: 1.875rem (30px)
- **font-weight-normal**: 400
- **font-weight-medium**: 500
- **font-weight-semibold**: 600
- **font-weight-bold**: 700

### Animation Tokens
- **transition-fast**: 150ms ease-out
- **transition-normal**: 300ms ease-out
- **transition-slow**: 500ms ease-out
- **ease-standard**: cubic-bezier(0.4, 0, 0.2, 1)
- **ease-emphasized**: cubic-bezier(0.2, 0.8, 0.2, 1)

## Component Variants

### Button Variants
- **primary**: Gradient background, white text, hover effect
- **secondary**: Outline style with gradient border, transparent background
- **tertiary**: Text-only button with gradient text
- **disabled**: Reduced opacity, no interactive effects

### Card Variants
- **standard**: Elevated card with shadow and rounded corners
- **gradient-border**: Card with gradient border accent
- **interactive**: Hover state with subtle lift effect

### Input Variants
- **default**: Standard input with gradient focus ring
- **invalid**: Input with error state styling
- **valid**: Input with success state styling

## Animation States

### Reduced Motion Preference
- **reduced-motion**: Disable all non-essential animations
- **essential-motion**: Allow only critical functional animations

### Component Animation States
- **hover**: Subtle scale or color shift
- **focus**: Gradient outline or glow effect
- **active**: Pressed state with deeper interaction
- **loading**: Skeleton or spinner animations
- **transition**: Page and layout transitions