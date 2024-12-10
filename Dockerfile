FROM python:slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install gunicorn

RUN apt-get -y update && \
  apt-get -y install ffmpeg


COPY . /app

ENTRYPOINT ["python"]

CMD [ "frontend.py" ]


