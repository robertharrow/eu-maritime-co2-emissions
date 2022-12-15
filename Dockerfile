FROM python:3.8

RUN apt-get update
RUN apt-get install nano

RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .
COPY data/ .
COPY app/countries.geojson .
RUN pip3 install -r requirements.txt

COPY app/ ./

CMD [ "gunicorn", "--timeout=120","--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
