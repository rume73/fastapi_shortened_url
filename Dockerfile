FROM python:3.10

RUN apt-get update && apt-get install -y netcat

WORKDIR /src

COPY ./requirements.txt .

COPY ./.env .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ADD ./src .
ADD ./scripts /scripts/

RUN chmod +x /scripts/start.sh

EXPOSE 8000
