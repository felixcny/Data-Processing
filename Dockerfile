FROM python:3.11-slim

WORKDIR /opt/dagster/app

# Installation des outils de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installation des libs Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Configuration de l'environnement
ENV DAGSTER_HOME=/opt/dagster/app
ENV DBT_PROFILES_DIR=/opt/dagster/app/dbt_project

EXPOSE 3000

# Commande magique : on pointe vers le fichier de l'étape 2
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-f", "src/definition.py"]