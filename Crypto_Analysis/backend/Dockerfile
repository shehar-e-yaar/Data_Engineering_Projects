# Python ka lightweight version use kar rahe hain
FROM python:3.10-slim

# Container ke andar working directory set kar rahe hain
WORKDIR /app

# Requirements file copy karna aur install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baqi sara code (Django project aur model) copy karna
COPY . .