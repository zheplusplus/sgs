import os

def serve(path, start_response):
    path = os.path.join(os.path.dirname(__file__), path)
    try:
        with open(path) as f:
            start_response('200 OK', [('Content-type', 'text/plain')])
            return f.readlines()
    except IOError:
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [path]
