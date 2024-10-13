import './globals.css'

export const metadata = {
  title: 'PixelProse AI',
  description: 'Conversational Image Recognition Chatbot',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}