export default function ResponseDisplay({ chatHistory }) {
    return (
      <div className="mt-4 bg-gray-100 rounded-lg p-4 h-96 overflow-y-auto">
        {chatHistory.map((entry, index) => (
          <div
            key={index}
            className={`mb-2 p-2 rounded-lg ${
              entry.type === 'user' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
            }`}
          >
            <span className="font-bold">{entry.type === 'user' ? 'You: ' : 'AI: '}</span>
            {entry.content}
          </div>
        ))}
      </div>
    )
  }