/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Datakick
        brand: {
          night:   '#1A1A2E', // Azul noche — fondo principal
          dark:    '#16213E', // Variante oscura
          mid:     '#0F3460', // Azul medio
          accent:  '#00D4AA', // Verde dato — acento principal
          'accent-dark': '#00A888',
          muted:   '#8892A4', // Texto secundario
          surface: '#1E2640', // Cards / superficies
          border:  '#2A3350', // Bordes
        },
        // Semánticos
        success: '#00D4AA',
        warning: '#F59E0B',
        danger:  '#EF4444',
      },
      fontFamily: {
        sans:  ['Inter', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'monospace'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        '2xs': ['0.65rem', { lineHeight: '1rem' }],
      },
      backgroundImage: {
        'grid-pattern': `linear-gradient(rgba(0,212,170,0.03) 1px, transparent 1px),
                         linear-gradient(90deg, rgba(0,212,170,0.03) 1px, transparent 1px)`,
      },
      backgroundSize: {
        'grid': '40px 40px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { opacity: '0', transform: 'translateY(12px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
