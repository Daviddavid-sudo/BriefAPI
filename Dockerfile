FROM python:3.11-slim

WORKDIR /app

# Installer la bibliothèque manquante (libgomp1)
RUN apt-get update && apt-get install -y libgomp1

ENV PYTHONUNBUFFERED=1 \
    ODBCINI=/etc/odbc.ini \
    ACCEPT_EULA=Y

# Copier et exécuter le script d'installation des drivers SQL Server
COPY install_sql_driver.sh install_sql_driver.sh
RUN chmod +x ./install_sql_driver.sh && ./install_sql_driver.sh

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000


CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "1"]