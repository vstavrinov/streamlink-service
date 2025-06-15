FROM alpine
WORKDIR /srv/streamlink-service
ENV TMPDIR=/dev/shm
ADD main.py gunicorn.conf.py ./
RUN apk update &&                                                       \
    apk add --no-cache python3 py-pip py-flask py3-gunicorn git tzdata; \
    pip --no-cache-dir install --break-system-packages                  \
        git+https://github.com/vstavrinov/streamlink.git;               \
    apk del git
CMD gunicorn --workers ${WORKERS:=2} --bind 0.0.0.0:${PORT:=8080} main:app
