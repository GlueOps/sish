FROM python:3-alpine

# Install Flask and Gunicorn
RUN pip install flask gunicorn

WORKDIR /app
COPY auth.py /app/auth.py

# Create data directory
RUN mkdir -p /data

# Run Gunicorn with 4 workers for multi-threading
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "auth:app"]