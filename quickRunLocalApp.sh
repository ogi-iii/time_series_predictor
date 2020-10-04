#! /bin/bash -eu
cd appContainer/
# Docker
docker image build -t tsp/app:latest .
docker container run -p 80:80 --rm tsp/app:latest
cd ../
