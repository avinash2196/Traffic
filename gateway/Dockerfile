FROM python:3.11-slim

WORKDIR /app

# Copy requirements (create if doesn't exist)
RUN echo "flask==3.0.0\nflask-cors==4.0.0\nrequests==2.31.0\naiofiles==23.2.1" > requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY gateway.py agw_protocol.py .
COPY .env .env 2>/dev/null || true

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

EXPOSE 5000

CMD ["python", "gateway.py"]
