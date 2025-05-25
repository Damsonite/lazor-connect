import { vars } from 'nativewind';

const colors = {
  primary: {
    light: '#7C3AED', // Púrpura intenso y moderno (vínculo, creatividad)
    dark: '#C084FC', // Lavanda brillante (curioso y accesible)
  },
  secondary: {
    light: '#06B6D4', // Cian vibrante (fluidez, conexión)
    dark: '#22D3EE',
  },
  accent: {
    light: '#F97316', // Naranja coral (energía, impulso)
    dark: '#FB923C',
  },
  text: {
    light: '#0F172A', // Muy oscuro pero con un tinte azul (tech)
    dark: '#F8FAFC', // Blanco azulado
  },
  background: {
    light: '#F1F5F9', // Gris azulado claro (neutro pero con vida)
    dark: '#0F172A', // Azul casi negro (profundidad)
  },
  confirm: {
    light: '#22C55E', // Verde más brillante (acción, éxito)
    dark: '#4ADE80',
  },
  danger: {
    light: '#EF4444', // Rojo intenso pero moderno
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
    '--color-confirm': colors.confirm.light,
    '--color-danger': colors.danger.light,
  }),
  dark: vars({
    '--color-primary': colors.primary.dark,
    '--color-secondary': colors.secondary.dark,
    '--color-accent': colors.accent.dark,
    '--color-text': colors.text.dark,
    '--color-background': colors.background.dark,
    '--color-confirm': colors.confirm.dark,
    '--color-danger': colors.danger.dark,
  }),
};

type Color = 'primary' | 'secondary' | 'accent' | 'text' | 'background' | 'confirm' | 'danger';

const withOpacity = (color: Color, opacity: number, mode: 'light' | 'dark') => {
  const hex = colors[color][mode];
  const alpha = Math.round(opacity * 255)
    .toString(16)
    .padStart(2, '0');

  return hex + alpha;
};

export { Color, colors, themes, withOpacity };
