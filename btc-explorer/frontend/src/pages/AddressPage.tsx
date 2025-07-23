import { useEffect, useState } from 'react'
import axios from 'axios'
import TxVolumeChart from '../components/TxVolumeChart'

interface Props {
  address: string
}

interface AddressInfo {
  balance: number
  total_received: number
  total_sent: number
  tx_count: number
  txs: any[]
}

export default function AddressPage({ address }: Props) {
  const [info, setInfo] = useState<AddressInfo | null>(null)
  const [volume, setVolume] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError('')
      
      try {
        const [infoRes, volumeRes] = await Promise.all([
          axios.get(`/api/address/${address}`),
          axios.get(`/api/address/${address}/volume-daily`)
        ])
        
        setInfo(infoRes.data)
        setVolume(volumeRes.data)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch address data')
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [address])

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        <p className="font-semibold">Error</p>
        <p>{error}</p>
      </div>
    )
  }

  if (!info) return null

  const handleExportCSV = async () => {
    try {
      const response = await axios.get(`/api/address/${address}/export-csv`, {
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${address}-volume.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error('Failed to export CSV:', err)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Address Details</h2>
        <p className="text-sm text-gray-600 break-all mb-4">{address}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Balance</p>
            <p className="text-xl font-semibold">{info.balance.toFixed(8)} BTC</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Total Received</p>
            <p className="text-xl font-semibold">{info.total_received.toFixed(8)} BTC</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Total Sent</p>
            <p className="text-xl font-semibold">{info.total_sent.toFixed(8)} BTC</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Transaction Count</p>
            <p className="text-xl font-semibold">{info.tx_count.toLocaleString()}</p>
          </div>
        </div>
      </div>

      {volume.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold text-gray-800">Transaction Volume History</h3>
            <button
              onClick={handleExportCSV}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              Export CSV
            </button>
          </div>
          <div className="h-64">
            <TxVolumeChart data={volume} />
          </div>
        </div>
      )}

      {info.txs && info.txs.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Recent Transactions</h3>
          <div className="space-y-2">
            {info.txs.slice(0, 10).map((tx: any) => (
              <div key={tx.hash} className="border-b pb-2">
                <p className="text-sm font-mono text-gray-600">{tx.hash}</p>
                <p className="text-sm text-gray-500">
                  {new Date(tx.time * 1000).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
