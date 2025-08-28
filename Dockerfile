# Imagen base con Python y uv ya incluido
FROM python:3.12-slim



# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv

RUN pip install uv
# Variables de entorno recomendadas para producción
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Crear directorio de la app
WORKDIR /app
# Copiar el código de la aplicación
COPY . .

# Instalar el proyecto 
RUN uv pip install --system -e .


# Comando de inicio con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
