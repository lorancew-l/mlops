#!/bin/bash
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

sed 's/localhost/host.docker.internal/g' .env > .container_env

docker-compose up -d
docker build -t train_model . -f Dockerfile.experiments