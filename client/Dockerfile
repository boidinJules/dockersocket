FROM python:3.9-slim

# Installer les bibliothèques nécessaires pour Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier le fichier client
COPY client.py .

# Commande pour exécuter le client
CMD ["python", "client.py"]
