import type { Metadata } from 'next'
import { Montserrat } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header/Header'
import Navbar from '@/components/Navbar/Navbar'
import Menu from '@/components/Menu/Menu'

const montserrat = Montserrat({ subsets: ['latin'] })

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

      <body className={montserrat.className}>
        <Header />

        <div className='conten-layout'>
          <Navbar />
          {children}
        </div>
        <Menu />
      </body>
    </html>
  )
}
