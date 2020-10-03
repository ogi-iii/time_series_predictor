#! /bin/bash
cd appContainer/
# Docker
docker image build -t tsp/app:latest .
docker container run -p 8000:8000 --rm tsp/app:latest
cd ../
