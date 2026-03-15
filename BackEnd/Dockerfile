FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc y forzar logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema requeridas para postgresql (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Variable de entorno de puerto para Render (sobreescribe si existe)
ENV PORT=8000
ENV HOST=0.00.0.0

# Comando para iniciar la aplicación (asegúrate de que uvicorn esté en tus requirements)
# Forzamos host 0.0.0.0 para que Render pueda hacer proxy al contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
