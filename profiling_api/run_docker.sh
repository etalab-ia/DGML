echo "Build image"
docker build -t pandas-profiling-api .

echo "Run container"
docker run -d -p 8080:80 -e MAX_WORKERS="2" -v /full/path/to/cache.sqlite:/app/cache.sqlite pandas-profiling-api
