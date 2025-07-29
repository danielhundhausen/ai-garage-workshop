# Azure App Deployment

```bash
az webapp up --name garage_workshop_agnet_handson --resource-group aigarage_apps --runtime "PYTHON:3.12"
az webapp config appsettings set --resource-group aigarage_apps --name garage_workshop_agnet_handson --settings WEBSITE_RUN_FROM_PACKAGE="1"
az webapp deploy --resource-group aigarage_apps --name garage_workshop_agnet_handson --src-path broker.zip
```
