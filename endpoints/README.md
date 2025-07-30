# Azure App Deployment

```bash
az webapp create --name garage-workshop-agent-handson --resource-group garage-workshop-agent-handson_group --runtime "PYTHON:3.12"
az webapp config set --resource-group garage-workshop-agent-handson_group --name garage-workshop-agent-handson --startup-file "uvicorn main:app --host=0.0.0.0 --port=\$PORT"
az webapp deploy --resource-group garage-workshop-agent-handson_group --name garage-workshop-agent-handson --src-path broker.zip
```
