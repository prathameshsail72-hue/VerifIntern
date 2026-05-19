FROM python:3.10-slim

# Install system dependency required by python-whois
RUN apt-get update && apt-get install -y whois && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make start script executable
RUN chmod +x start.sh

# Cloud Run sets the PORT environment variable (default 8080)
EXPOSE 8080

# Run both FastAPI and Streamlit
CMD ["./start.sh"]
