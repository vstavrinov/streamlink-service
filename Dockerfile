FROM alpine
WORKDIR /srv/streamlink-service
ENV COLUMNS=116
ADD stream.py .
RUN apk update &&                                                               \
    apk add uwsgi-python3 uwsgi-http py3-flask gcc musl-dev;                    \
    pip3 install https://github.com/vstavrinov/streamlink/archive/maverick.zip; \
    apk del gcc musl-dev;                                                       \
    rm -vfr /root/.cache /var/cache/apk/*
USER uwsgi
CMD uwsgi --plugin python3,http --http-socket 0.0.0.0:$PORT --wsgi-file stream.py --callable app -M -p 4 --threads 4
