FROM python:alpine
WORKDIR /webapp
COPY requirements.txt requirements.txt
RUN apk update
RUN pip install --no-cache-dir -r requirements.txt
COPY . /webapp/

