import { useState } from 'react'
import AddressPage from './pages/AddressPage'
import './index.css'

function App() {
  const [address, setAddress] = useState('')
  const [input, setInput] = useState('')
  const [error, setError] = useState('')

  const handleSearch = () => {
    // Basic Bitcoin address validation
    const btcAddressRegex = /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$/
    
    if (!input.trim()) {
      setError('Please enter a Bitcoin address')
      return
    }
    
    if (!btcAddressRegex.test(input.trim())) {
      setError('Invalid Bitcoin address format')
      return
    }
    
    setError('')
    setAddress(input.trim())
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto p-4">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">BTC Explorer</h1>
          <p className="text-gray-600">Explore Bitcoin addresses and transactions</p>
        </header>
        
        <div className="max-w-2xl mx-auto mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex gap-2">
              <input 
                value={input} 
                onChange={e => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter Bitcoin address (e.g., 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa)" 
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button 
                onClick={handleSearch}
                className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                Search
              </button>
            </div>
            {error && (
              <p className="mt-2 text-red-500 text-sm">{error}</p>
            )}
          </div>
        </div>
        
        {address && <AddressPage address={address} />}
      </div>
    </div>
  )
}

export default App
