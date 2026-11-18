# Démarrer les conteneurs
start:
	docker compose up -d --build

# Télécharger les données et les convertir en Parquet
collecte:
	docker compose exec jupyter bash script/telecharger_donnees.sh

# Arrêter les conteneurs
stop:
	docker compose down