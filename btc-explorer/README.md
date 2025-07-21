# BTC Explorer

A simple full-stack application to view Bitcoin address and transaction data with FastAPI and React.

## Backend

- **Run locally**
  ```bash
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```

## Frontend

- **Run locally**
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

The frontend proxies API requests to `localhost:8000` during development.

## Deployment

The repository includes a `vercel.json` for deploying both the FastAPI backend and React frontend to Vercel.
