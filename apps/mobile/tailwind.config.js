/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,tsx}', './components/**/*.{js,ts,tsx}'],

  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        accent: 'var(--color-accent)',
        text: 'var(--color-text)',
        background: 'var(--color-background)',
        confirm: 'var(--color-confirm)',
        danger: 'var(--color-danger)',
      },
      fontFamily: {
        orbitron: ['Orbitron', 'sans-serif'],
        itregular: ['InterRegular', 'sans-serif'],
        itmedium: ['InterMedium', 'sans-serif'],
        exmedium: ['ExoMedium', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
