/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        cyber: {
          black: '#0a0a0b',
          dark: '#161618',
          border: '#27272a',
          accent: '#3b82f6', // Security Blue
          danger: '#ef4444', // Breach Red
          success: '#22c55e' // Safe Green
        }
      }
    },
  },
  plugins: [],
}