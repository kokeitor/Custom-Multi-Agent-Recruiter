# Usa la imagen oficial de Python 3.11.6 como base
FROM python:3.11-slim

# Instala Rust y Cargo
RUN apt-get update && apt-get install -y \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . ~/.cargo/env \
    && rustup default stable

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor en /app
COPY . /app

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8052 para Streamlit
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "--server.port", "8000", "src/streamlit.py"]
