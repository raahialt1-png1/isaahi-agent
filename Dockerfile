# Use the official Playwright image (has the browser pre-installed!)
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set the working directory inside the server
WORKDIR /app

# Copy your requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code (app.py)
COPY . .

# Railway dynamically assigns a PORT variable. We tell Gunicorn to use it.
CMD gunicorn app:app -b 0.0.0.0:$PORT
