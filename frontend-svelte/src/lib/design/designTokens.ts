/**
 * AutoVault Design Tokens
 * Derived from DESIGN-linear.app.md specification.
 * Supports dual-theme (dark + light).
 */

export const colors = {
  dark: {
    // Brand & Accent
    primary: '#5e6ad2',
    'on-primary': '#ffffff',
    'primary-hover': '#828fff',
    'primary-focus': '#5e69d1',

    // Surface ladder
    canvas: '#010102',
    'surface-1': '#0f1011',
    'surface-2': '#141516',
    'surface-3': '#18191a',
    'surface-4': '#191a1b',

    // Borders
    hairline: '#23252a',
    'hairline-strong': '#34343a',
    'hairline-tertiary': '#3e3e44',

    // Text
    ink: '#f7f8f8',
    'ink-muted': '#d0d6e0',
    'ink-subtle': '#8a8f98',
    'ink-tertiary': '#62666d',

    // Semantic
    'semantic-success': '#27a644',
    'semantic-warning': '#f59e0b',
    'semantic-error': '#ef4444',
    'semantic-info': '#3b82f6',
    'semantic-overlay': 'rgba(0, 0, 0, 0.5)',
  },
  light: {
    // Brand & Accent
    primary: '#5e6ad2',
    'on-primary': '#ffffff',
    'primary-hover': '#4850b8',
    'primary-focus': '#5e69d1',

    // Surface ladder (inverted for light mode)
    canvas: '#f8f9fc',
    'surface-1': '#ffffff',
    'surface-2': '#f5f6f6',
    'surface-3': '#edeef0',
    'surface-4': '#e5e6e8',

    // Borders
    hairline: '#e2e4e9',
    'hairline-strong': '#d0d3d9',
    'hairline-tertiary': '#c5c8cf',

    // Text
    ink: '#1a1c20',
    'ink-muted': '#3d4147',
    'ink-subtle': '#6b7280',
    'ink-tertiary': '#9ca3af',

    // Semantic
    'semantic-success': '#16a34a',
    'semantic-warning': '#d97706',
    'semantic-error': '#dc2626',
    'semantic-info': '#2563eb',
    'semantic-overlay': 'rgba(0, 0, 0, 0.3)',
  },
} as const;

export const typography = {
  fontFamily: {
    display: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif",
    text: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif",
    mono: "'JetBrains Mono', 'SF Mono', 'Fira Code', ui-monospace, monospace",
  },
  scale: {
    'display-xl': { size: '80px', weight: 600, lineHeight: 1.05, letterSpacing: '-3.0px' },
    'display-lg': { size: '56px', weight: 600, lineHeight: 1.1, letterSpacing: '-1.8px' },
    'display-md': { size: '40px', weight: 600, lineHeight: 1.15, letterSpacing: '-1.0px' },
    headline: { size: '28px', weight: 600, lineHeight: 1.2, letterSpacing: '-0.6px' },
    'card-title': { size: '22px', weight: 500, lineHeight: 1.25, letterSpacing: '-0.4px' },
    subhead: { size: '20px', weight: 400, lineHeight: 1.4, letterSpacing: '-0.2px' },
    'body-lg': { size: '18px', weight: 400, lineHeight: 1.5, letterSpacing: '-0.1px' },
    body: { size: '16px', weight: 400, lineHeight: 1.5, letterSpacing: '-0.05px' },
    'body-sm': { size: '14px', weight: 400, lineHeight: 1.5, letterSpacing: '0' },
    caption: { size: '12px', weight: 400, lineHeight: 1.4, letterSpacing: '0' },
    button: { size: '14px', weight: 500, lineHeight: 1.2, letterSpacing: '0' },
    eyebrow: { size: '13px', weight: 500, lineHeight: 1.3, letterSpacing: '0.4px' },
    mono: { size: '13px', weight: 400, lineHeight: 1.5, letterSpacing: '0' },
  },
} as const;

export const spacing = {
  xxs: '4px',
  xs: '8px',
  sm: '12px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  xxl: '48px',
  section: '96px',
} as const;

export const rounded = {
  xs: '4px',
  sm: '6px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  xxl: '24px',
  pill: '9999px',
  full: '9999px',
} as const;

export const transitions = {
  fast: '120ms ease',
  base: '200ms ease',
  slow: '300ms ease',
  spring: '300ms cubic-bezier(0.34, 1.56, 0.64, 1)',
} as const;

export const breakpoints = {
  mobile: '480px',
  mobileLg: '768px',
  tablet: '1024px',
  desktop: '1280px',
  desktopXl: '1440px',
} as const;
