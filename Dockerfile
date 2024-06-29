# Utilisation d'une image Python de base
FROM python:3.9-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY main.py .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour démarrer le bot Discord
CMD ["python", "main.py"]