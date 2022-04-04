FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
