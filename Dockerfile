FROM python:3.6-alpine
LABEL maintainer="Kunal Malhotra, kunal.malhotra3@ibm.com"
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install cython \
 && pip install -r requirements.txt --default-timeout=100 future \
 && apk del .build-deps
COPY . .
EXPOSE 8000
CMD ["gunicorn","--bind localhost:5000","__init__:app"]