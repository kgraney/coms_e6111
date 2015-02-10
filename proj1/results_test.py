# -*- coding: latin-1 -*-
# pylint: disable=missing-docstring
import BaseHTTPServer
import contextlib
import functools
import socket
import threading
import unittest
import SocketServer

import results

SAMPLE_RESULT = u"""{"__metadata":{"uri":"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query=\u0027gates\u0027&$skip=0&$top=1","type":"WebResult"},"ID":"4251a261-fb62-4b3f-a645-28ac50fd07c9","Title":"Gates Corporation","Description":"Gates Corporation is Powering Progress™ in the Oil & Gas, Energy, Mining, Marine, Agriculture, Transportation and Automotive Industries.","DisplayUrl":"www.gates.com","Url":"http://www.gates.com/"}"""  # pylint: disable=line-too-long

@contextlib.contextmanager
def http_server(handler):
    """Context manager for having a BaseHTTPRequestHandler serving."""
    def url(port, path):
        return 'http://%s:%s%s' % (socket.gethostname(), port, path)
    httpd = SocketServer.TCPServer(("", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.setDaemon(True)
    thread.start()
    port = httpd.server_address[1]
    yield functools.partial(url, port)
    httpd.shutdown()

class TestBingResult(unittest.TestCase):

    def test_build_from_json(self):
        result = results.BingResult.build_from_json(SAMPLE_RESULT)
        self.assertEqual(u'http://www.gates.com/', result.url)
        self.assertEqual(u'Gates Corporation', result.title)
        self.assertEqual(
            u'Gates Corporation is Powering Progress™ in the Oil & Gas, Energy, '
            'Mining, Marine, Agriculture, Transportation and Automotive '
            'Industries.', result.description)

    def test_get_page_contents(self):
        class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.wfile.write("\n" + "blah clah <b>dlah</b> <script a=\"b\">some stuff</script>")

        with http_server(Handler) as url:
            result = results.BingResult(title="Some title",
                                        description="Some description",
                                        url=url("/"))
            self.assertEqual("blah clah dlah", result.get_page_contents())


if __name__ == '__main__':
    unittest.main(verbosity=2)
