import type { Metadata } from 'next'
import { Montserrat } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header/Header'

const inter = Montserrat({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'mbrw',
  description: 'game insider',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">

      <body className={inter.className}>
        <Header />{children}</body>
    </html>
  )
}
