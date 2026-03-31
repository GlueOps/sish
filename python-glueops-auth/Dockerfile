FROM python:3.13-alpine@sha256:bb1f2fdb1065c85468775c9d680dcd344f6442a2d1181ef7916b60a623f11d40

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth.py .

RUN mkdir -p /data

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "auth:app"]