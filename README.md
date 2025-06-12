# streamlink-service

This video streaming service based on [streamlink](https://github.com/streamlink/streamlink) project. It extracts stream from web page and feeds it directly to Your video player allowing to avoid using browser. You can run it either on local computer or on the cloud turning it into global service.

## Simplest Quik Start

```
docker run -p 8080:8080 vstavrinov/streamlink-service
```

## Build:

```
git clone https://github.com/vstavrinov/streamlink-service.git
cd streamlink-service
docker build -t streamlink-service .
```

## Usage:

```
docker run -d -e WORKERS=<workers-number> -e PORT=<service-port> -p <container-port>:<service-port> <streamlink-image>
```

- service-port is port of service inside container (default 8080).
- container-port is where you send your request for stream
- streamlink-image is either docker image You build on your own or those pulled from repository.
- workers-number is max clients served simultaneously (default 2).

For example:

```
docker run -d -e PORT=8080 -p 8080:8080 streamlink-service
```
Or you can omit build phase and pull and run it directly from repository:

```
docker run -d -e PORT=8080 -p 8080:8080 vstavrinov/streamlink-service
```

Finally you can watch tv:

```
vlc --playlist-autostart http://localhost:8080/?youtube.com/user/Bloomberg+best=
```

Here 'youtube.com/user/Bloomberg' is URL of web page where You watch this stream with browser. Trailing '=' sign is necessary in this case because it is shortcut for 'url=youtube.com/user/Bloomberg+best' parameter. The '+best'  suffix  is one of available streams. Check for all available streams:

```
curl http://localhost:8080/?youtube.com/user/Bloomberg=
```

Here is list of supported sites for streaming: https://github.com/vstavrinov/streamlink/blob/master/docs/plugin\_matrix.rst

See more available options:

```
curl http://localhost:8080/?help=
```

You can put these options into query string with '&' delimiter in the form: 
```
key1=value1&key2=value2
```
For example using proxy:
```
vlc --playlist-autostart 'http://localhost:8080/?youtube.com/user/Bloomberg+best=&https-proxy=http://80.245.117.194:8080'
```
If the URL itself contains query string then url should be set in key/value style like others i.e. url=...

For example:
```
vlc --playlist-autostart 'http://localhost:8080/?url=arconaitv.us/stream.php?id=44+best&http-ssl-verify='
```
The last example shows as well how to set boolean value: the key 'http-ssl-verify' has no value  - this way it set to False, while in any other ways it always gets True. Note that some sites requires username and password, so they could be added as usual options.

Needless to say You can use any player instead vlc and browser your prefer instead curl. 
