import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js'
import { useMemo } from 'react'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

interface Props {
  data: { date: string; volume: number }[]
}

export default function TxVolumeChart({ data }: Props) {
  const chartData = useMemo(() => {
    return {
      labels: data.map(d => d.date),
      datasets: [
        {
          label: 'Daily BTC Volume',
          data: data.map(d => d.volume),
          fill: false,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.5)',
          tension: 0.1,
        },
      ],
    }
  }, [data])

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            return `Volume: ${(context.parsed.y ?? 0).toFixed(8)} BTC`
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return value + ' BTC'
          }
        }
      }
    }
  }

  return <Line data={chartData} options={options} />
}
