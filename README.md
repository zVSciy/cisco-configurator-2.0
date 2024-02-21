<div align="center">

# Cisco-Configurator 2.0

</div>

## Run the container

Open the CLI and enter this command to build the container
```docker
docker build -t cisco-django-app .
```
Next step you need to run the container with the following command
```docker
docker run -it -p 8000:8000 cisco-django-app
```