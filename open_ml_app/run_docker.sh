echo "Remove image"
docker rm -f open-ml-app
echo "Build image"
docker build -t open-ml-app .

echo "Run container"
docker run -d -p 8050:80 --name open-ml-app --env-file ./.env open-ml-app