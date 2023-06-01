FROM python:3.10-alpine

WORKDIR /api

COPY api/ .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host 0.0.0.0" ]
