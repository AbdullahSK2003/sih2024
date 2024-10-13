'use client'

import { useState } from 'react'
import ChatInterface from '../components/ChatInterface'
import ImageUpload from '../components/ImageUpload'
import ResponseDisplay from '../components/ResponseDisplay'

export default function Home() {
  const [chatHistory, setChatHistory] = useState([])
  const [currentImage, setCurrentImage] = useState(null)

  const handleImageUpload = async (imageFile) => {
    const formData = new FormData()
    formData.append('file', imageFile)
    
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    setCurrentImage(data.url)
  }

  const handleSendMessage = async (message) => {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, imageUrl: currentImage }),
    })
    const data = await response.json()
    setChatHistory([...chatHistory, { type: 'user', content: message }, { type: 'bot', content: data.response }])
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-8">PixelProse AI</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <ImageUpload onUpload={handleImageUpload} />
          {currentImage && (
            <div className="mt-4">
              <img src={currentImage} alt="Uploaded" className="max-w-full h-auto rounded-lg shadow-md" />
            </div>
          )}
        </div>
        <div>
          <ChatInterface onSendMessage={handleSendMessage} />
          <ResponseDisplay chatHistory={chatHistory} />
        </div>
      </div>
    </main>
  )
}