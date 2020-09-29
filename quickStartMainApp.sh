#! /bin/bash

# Docker
docker image build -t tsp/app:latest .
docker container run -p 8000:8000 tsp/app:latest
