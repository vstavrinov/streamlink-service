from flask import Flask, request, Response
# We use streamlink to catch video stream from web page or direct link.
from streamlink import Streamlink
# Use cli to ouput help
from streamlink_cli.main import parser_helper

app = Flask(__name__)
# Set video chunk size
buff_size = 1 << 17


@app.route('/')
def main():
    # Get arguments passed with query string
    args = request.args
    # Output cli help
    if 'help' in args:
        return Response(parser_helper().format_help(), content_type='text/plain')
    # url should be either first argument or set explicitly with 'url' key.
    if 'url' not in args:
        url = next(iter(args))
    else:
        url = args['url']

    # Split url to url itself (url[0]) and stream (url[1]) if present.
    url = url.split()
    session = Streamlink()
    # Use remain arguments to set other options.
    for key in args:
        session.set_option(key, args[key])
    try:
        # Catch stream with given url
        streams = session.streams(url[0])
    except Exception as exception:
        error = 'Exception {0}: {1}\n'.format(type(exception).__name__, exception)
        return Response(error, content_type='text/plain')
    # pick the stream
    if len(url) > 1:
        stream = streams[url[1]]
    else:
        # If specific stream is not provided in args, output list of available streams.
        return Response('Available streams: ' + str(list(streams.keys())) + '\n', content_type='text/plain')

    # Stream generator
    def generate():
        # Open file like object of stream
        with stream.open() as fd:
            chunk = True
            # Iterate over stream
            while chunk:
                chunk = fd.read(buff_size)
                # Read chunk of stream
                yield chunk

    # Streaming to client
    return Response(generate(), content_type='video/mpeg')


# call script from command line for testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
