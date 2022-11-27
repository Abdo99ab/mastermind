FROM python:3.9.1

ENV PYTHONUNBUFFERED=1

WORKDIR /django_rest

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
