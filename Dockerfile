FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fly.io listens on port 8080 by default
EXPOSE 8080

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
