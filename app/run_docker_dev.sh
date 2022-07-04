echo "Prepare conf"
cp conf.dev.json conf.json
echo "Remove image"
docker rm -f open-ml-app-dev
echo "Build image"
docker build -t open-ml-app-dev .

echo "Run container"
docker run -d -p 8051:80 --name open-ml-app-dev --env-file ./.env open-ml-app-dev
