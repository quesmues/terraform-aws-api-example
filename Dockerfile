FROM python:3.10

RUN apt-get update
RUN apt-get install -y awscli
RUN apt-get clean

COPY app/ /app

ARG AWS_SECRET_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

RUN aws configure set aws_access_key_id $AWS_SECRET_KEY_ID \
  && aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY \
  && aws configure set default.region $AWS_DEFAULT_REGION

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0" ]
