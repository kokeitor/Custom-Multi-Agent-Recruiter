FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit.py", "--server.port=8000", "--server.address=0.0.0.0"]

# Comando por defecto para ejecutar la aplicación Streamlit
# CMD ["streamlit", "run", "--server.port", "8000", "src/streamlit.py"]
# CMD ["python", "src/test2.py"]
