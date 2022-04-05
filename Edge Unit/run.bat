echo "Building and running"
docker build -t facerecognitionapi .
docker run -d -p 5055:5055 -e PYTHONUNBUFFERED=0 facerecognitionapi