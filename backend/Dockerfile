FROM python:3.11-slim
# Nastavení prostředí
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Instalace systémových závislostí
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Nastavení pracovního adresáře
WORKDIR /app
# Kopírování requirements.txt
COPY requirements.txt .
# Instalace Python závislostí
RUN pip install --no-cache-dir -r requirements.txt
# Kopírování aplikačního kódu
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Spuštění aplikace
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]