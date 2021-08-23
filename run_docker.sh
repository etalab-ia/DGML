#!/usr/bin/env bash
echo "Remove image"
docker rm -f dgml
echo "Build image"
docker build -t dgml .

echo "Run container"
#docker run  -p 8050:80 --name dgml dgml

#docker run  -p 80:80 -e PRE_START_PATH="/prestart.sh" -e MODULE_NAME="app.main" -e VARIABLE_NAME="server" --name dgml dgml
#docker run  -p 8050:80 --env-file ./deploy_docker.env --name dgml dgml
#docker run  -p 80:80 --name dgml dgml