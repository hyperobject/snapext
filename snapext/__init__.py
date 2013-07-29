# Copyright (C) 2013 Connor Hudson, Tim Radvan

"""Module for writing Snap! extensions.

Usage:

    import snapext

    handler = snapext.SnapHandler

    doors_open = True
    # Replace with library for spaceship door interaction

    @handler.route('/doors/set')
    def set_doors(open):
        global doors_open
        if open:
            doors_open = True
            # Open spaceship doors
        else:
            doors_open = False
            # Close spaceship doors -- don't let humans in!

    @handler.route('/doors/is_open')
    def get_doors():
        return doors_open

    # Run the server
    snapext.main(handler, 47543)

"""

__version__ = '0.1.3'

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from urlparse import urlsplit, parse_qs
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer



class SnapHandler(SimpleHTTPRequestHandler):
    """An HTTP server with Flask-style routing."""

    routes = {}

    special = {
        'true': True,
        'false': False,
    }

    @classmethod
    def prettify_arg(cls, value):
        value = cls.special.get(value, value)
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value # str

    def send_head(self):
        split_url = urlsplit(self.path)
        path = split_url.path
        args = parse_qs(split_url.query)
        args = dict((k, self.prettify_arg(v[0])) for (k, v) in args.items())
        print 'args', args

        if path in self.routes:
            f = self.routes[path]
            response = f(**args)
            response = "" if response is None else unicode(response)

            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Length", str(len(response)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            return StringIO(response)
        elif path == '/':
            return StringIO(self.index())
        else:
            self.send_error(404, "Path not found")

    @classmethod
    def add_route(self, path, f):
        """Same as the :meth:`route` decorator.

            @handler.route('/')
            def index():
                pass

        Is equivalent to:

            def index():
                pass
            handler.add_url_rule('/', 'index', index)

        """
        if path in self.routes and path != '/':
            raise ValueError, "route already exists"
        self.routes[path] = f

    @classmethod
    def route(self, path, **options):
        def decorator(f):
            self.add_route(path, f, **options)
            return f
        return decorator

    def index(self, path):
        """Return the list of routes in plain text format."""
        return "\n".join(sorted(self.routes))


class Server(TCPServer):
    allow_reuse_address = True


def main(handler, port, silent=False):
    """Runs the server for Snap! to connect to."""
    httpd = Server(("", port), handler)
    if not silent:
        print "Serving at port %i" % port
        print "Go ahead and launch Snap!"
    httpd.serve_forever()

