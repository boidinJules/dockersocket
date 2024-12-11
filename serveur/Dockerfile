# Utiliser une image Python officielle
FROM python:3.9-slim

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier server.py dans le conteneur
COPY server.py .

# Exposer le port utilisé par le serveur
EXPOSE 63000

# Commande pour exécuter le script server.py
CMD ["python", "server.py"]