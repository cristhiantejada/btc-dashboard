import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { useMemo } from 'react'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

interface Props {
  data: { date: string; volume: number }[]
}

export default function TxVolumeChart({ data }: Props) {
  const chartData = useMemo(() => {
    return {
      labels: data.map(d => d.date),
      datasets: [
        {
          label: 'BTC Volume',
          data: data.map(d => d.volume),
          fill: false,
          borderColor: 'rgb(75,192,192)',
        },
      ],
    }
  }, [data])

  return <Line data={chartData} />
}
