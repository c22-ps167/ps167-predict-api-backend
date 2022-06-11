FROM python:slim-buster

WORKDIR /app

COPY . /app

RUN python -m venv env

CMD ["source", "env/bin/activate"]

RUN pip install -r requirements.txt

ENTRYPOINT flask run