# Configurer le .env
Le `.env` doit être de la forme suivante :

```
export BASE_URL="https://${CODESPACE_NAME}-8080.app.github.dev"
export SPRING_SECURITY_OAUTH2_CLIENT_ID="votreClientID"
export SPRING_SECURITY_OAUTH2_CLIENT_SECRET="votreClientSecret"
export MY_GITHUB_PAT="votrePAT"
```

Une fois qu'il a été complété, il faut faire un `source .env` avant d'exécuter une application qui aurait besoin de ces variables d'environnement

# Exécuter l'appli

Pour compiler/exécuter en développement :
```
mvn clean install  ; mvn spring-boot:run
```

Pour exécuter les tests :
```
pytest tests
```