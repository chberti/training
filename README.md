# training
some training

## Etat Global

- API Flask qui expose une page simple sur l'endpoint /upload
- En cas le POST, le fichier est chargé et un check de type CSV est effectué
- Si c'est un CSV, alors on lance la fonction de traitement dans le module csv_importer
- Si vous vous rendez sur l'endpoint /person, vous aurez un .describe() du fichier csv chargé

### csv_importer

Le csv_importer va traiter la table contenue dans le CSV pour extraire des colonnes, générer des id uniques pour nos 3 tables, puis charger les 3 dataframes dans une abse de données PostgreSQL locale (voir docker-compose)

### xlsx_importer

Le xlsx_importer fait des opérations équivalentes au csv_importer. Pas encore testé de bout en bout.

## Build

```
#Construction image docker
docker build -t current_app .

#Lancement des conteneurs
docker-compose up
```

## TODO

- Traitement de fichiers xlsx en erreur pour le moment depuis l'API Flask. Mais la fonction coeur renvoi un résultat qui me semble bon.
- Mettre de côté les fonctions de connexion à la base de données
- Créer un fichier de configuration global de l'API Flask 