import re
import urllib.parse
from flask import Flask, request, Response
# We use streamlink to catch video stream from web page or direct link.
from streamlink import Streamlink
from streamlink.session.options import StreamlinkOptions
from sys import argv
from time import time
from urllib.request import urlopen

app = Flask(__name__)
# Set video chunk size
buff_size = 1 << 16
pause = 600


@app.route('/')
def streamlink(request=request):
    '''Parse query string, set options and get stream.'''
    try:
        # Get arguments passed with query string
        args = request.args
        # Available options
        if 'help' in args:
            return Response(StreamlinkOptions.__doc__, content_type='text/plain')
        if 'version' in args:
            return Response(Streamlink.version.fget('self') + '\n', content_type='text/plain')
        # url should be either first argument or set explicitly with 'url' key.
        if 'url' not in args:
            url = next(iter(args))
        else:
            url = args['url']

        # Split url to url itself (url[0]) and stream (url[1]) if present.
        url = urllib.parse.unquote(url).split()
        session = Streamlink()
        pluginname, pluginclass, resolved_url = session.resolve_url(url[0])
        # Use remain arguments to set other options.
        session.set_option('http-ssl-verify', 0)
        for key in args:
            if re.match('[0-9]+$', args[key]):
                value = int(args[key])
            else:
                value = args[key]
            # Set session options described by help
            session.set_option(key, value)
        # Set plugin options if require (usually username and password)
        options = session.options
        # Catch stream with given url
        pluginclass(session, resolved_url, options)
        streams = session.streams(url[0])
        # pick the stream
        if len(url) > 1:
            stream = streams[url[1]]
        else:
            # If specific stream is not provided in args, output list of available streams.
            return Response('Available streams: ' + str(list(streams.keys())) + '\n', content_type='text/plain')

        # Stream generator
        url_root = request.url_root

        def generate(fd):
            chunk = True
            # Iterate over stream
            with fd:
                last = time()
                while chunk:
                    now = time()
                    # yank periodically server to keepalive
                    if now - last > pause:
                        urlopen(url_root)
                        last = now
                    chunk = fd.read(buff_size)
                    # Read chunk of stream
                    yield chunk

        if 'link' in args:
            # Redirect client to stream url
            redirect_url = stream.url
            response = Response('', content_type='')
            response.headers['Location'] = redirect_url
            response.status_code = 302
            return response
        else:
            # Streaming to client
            # Open file like object of stream
            fd = stream.open()
            return Response(generate(fd), content_type='video/mpeg')
    except Exception or OSError as exception:
        error = 'Exception {0}: {1}\n'.format(type(exception).__name__, exception)
        return Response(error, content_type='text/plain')


# call script from command line for testing
if __name__ == '__main__':
    if len(argv) > 1:
        port = argv[1]
    else:
        port = 8080
    app.run(debug=True, host='0.0.0.0', port=port)
