FROM alpine
WORKDIR /srv/streamlink-service
ENV PORT=7000
EXPOSE $PORT
ADD main.py gunicorn.conf.py .
RUN apk update &&                                                \
    apk add --no-cache python3 py-pip py-flask py3-gunicorn git; \
    pip --no-cache-dir install                                   \
        git+https://github.com/vstavrinov/streamlink.git;        \
    apk del git
CMD gunicorn --bind 0.0.0.0:$PORT main:app
