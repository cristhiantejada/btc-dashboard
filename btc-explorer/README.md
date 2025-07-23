# BTC Explorer

A modern full-stack application to explore Bitcoin addresses and transactions, built with FastAPI and React.

## Features

- 🔍 Search Bitcoin addresses with validation
- 💰 View address balance, transaction count, and history
- 📊 Interactive charts showing daily transaction volumes
- 📥 Export transaction volume data as CSV
- 🚀 Fast and responsive UI with Tailwind CSS
- ⚡ Real-time data from blockchain.info API
- 🛡️ Error handling and loading states

## Tech Stack

- **Backend**: FastAPI, Python 3.8+, httpx
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
- **Charts**: Chart.js with react-chartjs-2
- **Deployment**: Configured for Vercel

## Project Structure

```
btc-explorer/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── routers/            # API route handlers
│   │   ├── address.py      # Address-related endpoints
│   │   └── tx.py           # Transaction endpoints
│   ├── services/           # Business logic
│   │   └── blockchain_api.py # Blockchain.info API client
│   └── utils/              # Utility functions
│       └── formatters.py   # Data formatting helpers
└── frontend/
    ├── src/
    │   ├── components/     # Reusable React components
    │   ├── pages/          # Page components
    │   └── App.tsx         # Main application component
    └── public/             # Static assets
```

## Backend Setup

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the development server**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`. View API documentation at `http://localhost:8000/docs`.

## Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the backend.

## API Endpoints

- `GET /` - API root with links to documentation
- `GET /healthz` - Health check endpoint
- `GET /api/address/{address}` - Get address information
- `GET /api/address/{address}/volume-daily` - Get daily transaction volumes
- `GET /api/address/{address}/export-csv` - Export volume data as CSV
- `GET /api/tx/{txid}` - Get transaction details
- `GET /api/stats/blockheight` - Get latest block height
- `GET /api/price` - Get current BTC price in USD

## Deployment

The project includes a `vercel.json` configuration for easy deployment to Vercel:

```bash
# From the btc-explorer directory
vercel
```

## Environment Variables

### Backend
- `BLOCKCHAIN_API_URL` - Blockchain.info API base URL (default: https://blockchain.info)
- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

### Frontend
- No additional configuration required for development

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.
