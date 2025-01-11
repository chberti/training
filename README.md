# training
some training

## Etat Global

- API Flask qui expose une page simple sur l'endpoint /upload
- En cas le POST, le fichier est chargé et un check de type CSV est effectué
- Si c'est un CSV, alors on lance la fonction de traitement dans le moudle csv_importer

### csv_importer

Le csv_importer va traiter la table contenue dans le CSV pour extraire des colonnes, générer des id uniques pour nos 3 tables, puis charger les 3 dataframes dans une abse de données PostgreSQL locale (voir docker-compose)

## Build

```
#Construction image docker
docker build -t current_app .

#Lancement des conteneurs
docker-compose up
```

## TODO

- Traiter les fichiers de type .xlsx