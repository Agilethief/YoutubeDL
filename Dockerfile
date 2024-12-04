FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn

COPY app app
