/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'infath-primary': '#1E3A8A',
        'infath-dark': '#1E40AF',
        'infath-light': '#3B82F6',
      },
      fontFamily: {
        'arabic': ['Arabic', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'infath': '0 4px 6px -1px rgba(30, 58, 138, 0.1), 0 2px 4px -1px rgba(30, 58, 138, 0.06)',
      },
    },
  },
  plugins: [],
} 