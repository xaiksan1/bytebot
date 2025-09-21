# Dockerfile pour le service 'blue_scanner'
# C'est ici que je suis installée et configurée.

# J'utilise une image Python légère et stable comme base pour mes opérations.
FROM python:3.12-alpine

# Je mets à jour les paquets du système pour corriger les vulnérabilités connues.
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

# Mon répertoire de travail à l'intérieur de mon environnement virtuel.
WORKDIR /app

# Je copie mes "outils" (dépendances Python) et je les installe pour être prête.
# Ce fichier 'requirements.txt' doit exister et lister mes besoins.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Je copie ensuite tout mon "code cérébral" (tes scripts Python) dans mon environnement.
COPY . .

# Enfin, je définis la commande que j'exécuterai par défaut quand tu me lanceras.
# C'est mon "point de départ" pour scanner Amazon.
# Tu peux changer 'scanner.py' par le nom du script principal que je devrai exécuter.
CMD ["python", "scanner.py"]