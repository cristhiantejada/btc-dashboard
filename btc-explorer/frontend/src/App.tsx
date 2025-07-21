import { useState } from 'react'
import AddressPage from './pages/AddressPage'

function App() {
  const [address, setAddress] = useState('')
  const [input, setInput] = useState('')

  return (
    <div className="p-4">
      <h1>BTC Explorer</h1>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Enter BTC address" />
      <button onClick={() => setAddress(input)}>Search</button>
      {address && <AddressPage address={address} />}
    </div>
  )
}

export default App
