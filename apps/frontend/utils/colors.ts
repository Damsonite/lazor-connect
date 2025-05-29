import { vars } from 'nativewind';

const colors = {
  primary: {
    light: '#7C3AED',
    dark: '#C084FC',
  },
  secondary: {
    light: '#EDE9FE',
    dark: '#191d35',
  },
  accent: {
    light: '#F97316',
    dark: '#FB923C',
  },
  text: {
    light: '#0F172A',
    dark: '#F8FAFC',
  },
  background: {
    light: '#F1F5F9',
    dark: '#0F172A',
  },
  gray: {
    light: '#E5E7EB',
    dark: '#2F3244',
  },
  confirm: {
    light: '#22C55E',
    dark: '#4ADE80',
  },
  danger: {
    light: '#EF4444',
    dark: '#F87171',
  },
};

const themes = {
  light: vars({
    '--color-primary': colors.primary.light,
    '--color-secondary': colors.secondary.light,
    '--color-accent': colors.accent.light,
    '--color-text': colors.text.light,
    '--color-background': colors.background.light,
    '--color-gray': colors.gray.light,
    '--color-confirm': colors.confirm.light,
    '--color-danger': colors.danger.light,
  }),
  dark: vars({
    '--color-primary': colors.primary.dark,
    '--color-secondary': colors.secondary.dark,
    '--color-accent': colors.accent.dark,
    '--color-text': colors.text.dark,
    '--color-background': colors.background.dark,
    '--color-gray': colors.gray.dark,
    '--color-confirm': colors.confirm.dark,
    '--color-danger': colors.danger.dark,
  }),
};

type Color =
  | 'primary'
  | 'secondary'
  | 'accent'
  | 'text'
  | 'background'
  | 'gray'
  | 'confirm'
  | 'danger';

const withOpacity = (color: Color, opacity: number, mode: 'light' | 'dark') => {
  const hex = colors[color][mode];
  const alpha = Math.round(opacity * 255)
    .toString(16)
    .padStart(2, '0');

  return hex + alpha;
};

export { Color, colors, themes, withOpacity };
