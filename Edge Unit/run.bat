echo "Building and running"
docker build -t facerecognitionapi .
docker run -d -p 5000:5000 -e PYTHONUNBUFFERED=0 facerecognitionapi