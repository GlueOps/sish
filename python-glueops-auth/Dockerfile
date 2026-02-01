FROM python:3.12-alpine@sha256:82585c9f05cf72b5975f110e9409596bcd16c70a45f38e5f36889823cc6fc071

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth.py .

RUN mkdir -p /data

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "auth:app"]