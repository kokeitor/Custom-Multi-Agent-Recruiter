# Usa la imagen oficial de Python 3.11.6 como base
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8052 para Streamlit
EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit.py", "--server.port=8000", "--server.address=0.0.0.0"]

# Comando por defecto para ejecutar la aplicación Streamlit
# CMD ["streamlit", "run", "--server.port", "8052", "src/streamlit.py"]
# CMD ["python", "src/test2.py"]
