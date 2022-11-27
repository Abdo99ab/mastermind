FROM python:3.9.1

ENV PYTHONUNBUFFERED=1

WORKDIR /flask_rest

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .