import { useEffect, useState } from 'react'
import axios from 'axios'
import TxVolumeChart from '../components/TxVolumeChart'

interface Props {
  address: string
}

export default function AddressPage({ address }: Props) {
  const [info, setInfo] = useState<any>()
  const [volume, setVolume] = useState<any[]>([])

  useEffect(() => {
    axios.get(`/api/address/${address}`).then(res => setInfo(res.data))
    axios.get(`/api/address/${address}/volume-daily`).then(res => setVolume(res.data))
  }, [address])

  if (!info) return <div>Loading...</div>

  return (
    <div>
      <h2>Address: {address}</h2>
      <p>Balance: {info.balance} BTC</p>
      <p>Total Received: {info.total_received} BTC</p>
      <p>Total Sent: {info.total_sent} BTC</p>
      <p>Tx Count: {info.tx_count}</p>
      <TxVolumeChart data={volume} />
    </div>
  )
}
