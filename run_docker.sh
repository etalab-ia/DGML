echo "Remove image"
docker rm -f dgml
echo "Build image"
docker build -t dgml .

echo "Run container"
docker run -d -p 8050:80 --name dgml-app dgml