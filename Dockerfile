FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add python3-dev gcc libressl-dev libc-dev libffi-dev
COPY . /image_scraping
WORKDIR /image_scraping
RUN pip install -r requirements.txt
ENTRYPOINT [ "sh", "entrypoint.sh" ]