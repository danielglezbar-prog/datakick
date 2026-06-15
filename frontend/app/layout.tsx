import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Datakick — Inteligencia de datos para La Quiniela',
  description: 'Motor analítico avanzado para La Quiniela. Análisis pre-jornada, bombazos estadísticos y rentabilidad esperada. El edge que necesitas.',
  keywords: ['quiniela', 'análisis quiniela', 'estadísticas fútbol', 'quiniela IA', 'pronosticos quiniela'],
  authors: [{ name: 'Datakick' }],
  openGraph: {
    title: 'Datakick — Inteligencia de datos para La Quiniela',
    description: 'Motor analítico avanzado para La Quiniela española.',
    url: 'https://datakick.es',
    siteName: 'Datakick',
    locale: 'es_ES',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Datakick',
    description: 'Motor analítico para La Quiniela',
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" className="dark">
      <body className="min-h-screen antialiased">
        {children}
      </body>
    </html>
  )
}
