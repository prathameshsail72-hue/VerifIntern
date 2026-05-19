#!/bin/bash

# Start FastAPI backend in the background on port 8000
echo "Starting FastAPI backend..."
uvicorn main:app --host 127.0.0.1 --port 8000 &

# Start Streamlit frontend in the foreground on the Cloud Run provided port
echo "Starting Streamlit frontend..."
export API_URL="http://127.0.0.1:8000/api"
streamlit run frontend/app.py --server.port=${PORT:-8080} --server.address=0.0.0.0
