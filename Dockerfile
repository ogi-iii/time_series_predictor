FROM python:3.7

RUN apt-get update

COPY ./app /

RUN pip install -r requirements.txt

EXPOSE 8000

# fixed commands with "docker run"
ENTRYPOINT ["python", "app.py"]
# default params after ENTRYPOINT
# CMD ["YOUR TSPUploadLambdaApi Endpoint", "YOUR TSPHistoryLambdaApi Endpoint"]
