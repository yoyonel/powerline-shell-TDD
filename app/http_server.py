from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import SocketServer
from tools.tools import is_unsigned_integer
import re
import simplejson
import cgi


# urls:
# - https://docs.python.org/3/glossary.html#term-global-interpreter-lock
# - http://stackoverflow.com/questions/1312331/using-a-global-dictionary-with-threads-in-python
# - http://stackoverflow.com/questions/105095/are-locks-unnecessary-in-multi-threaded-python-code-because-of-the-gil
# - https://docs.python.org/3/library/dis.html#opcode-STORE_SUBSCR
# -> au final, sur des operations "aussi courtes", l'interpreteur python est deja protege.

class LocalDataWithoutMutex(object):
    """

    """
    _records = {}

    @staticmethod
    def get_record(id_record):
        """

        """
        return LocalDataWithoutMutex._records[id_record]

    @staticmethod
    def set_record(id_record, record_):
        """

        """
        LocalDataWithoutMutex._records[id_record] = record_


class LocalDataWithMutex(object):
    """

    """
    _lock = threading.Lock()
    _records = {}

    @staticmethod
    def get_record(id_record):
        """
        Mutex safe (static) method to get a record

        :param id_record:
        :return:
        """

        with LocalDataWithMutex._lock:
            record = LocalDataWithMutex._records[id_record]
        return record

    @staticmethod
    def set_record(id_record, record_):
        """
        Mutex safe (static) method to set a record
        """
        with LocalDataWithMutex._lock:
            LocalDataWithMutex._records[id_record] = record_


LocalData = LocalDataWithoutMutex
# LocalData = LocalData_with_Mutex


class HTTPRequestHandler(BaseHTTPRequestHandler, object):
    """

    """
    @staticmethod
    def get_suffix(prefix, path):
        """

        :param prefix:
        :param path:
        :return:
        """
        # urls:
        # - https://docs.python.org/2/library/re.html
        # - http://stackoverflow.com/questions/12572362/get-a-string-after-a-specific-substring
        m = re.search('(?:'+prefix+')(.*)', path)
        return m.group(1)

    @staticmethod
    def get_path_for_POST():
        """

        :return:
        """
        return 'api/v1/addrecord/'

    @staticmethod
    def get_path_for_GET():
        """

        :return:
        """
        return 'api/v1/getrecord/'

    @staticmethod
    def get_pattern_for_POST():
        return HTTPRequestHandler.get_path_for_POST() + '*'

    @staticmethod
    def get_pattern_for_GET():
        return HTTPRequestHandler.get_path_for_GET() + '*'

    def _send_response_with_end_headers(self, status_code, msg=None):
        """

        :param status_code:
        :param msg:
        :return:
        """
        self.send_response(status_code, msg)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        """

        :return:
        """
        pattern_for_POST = self.get_pattern_for_POST()
        if re.search(pattern_for_POST, self.path) is not None:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = self.rfile.read(length)
                # url: http://stackoverflow.com/questions/31371166/reading-json-from-simplehttpserver-post-data
                data_json = simplejson.loads(data)
                recordID = self.get_suffix(self.get_path_for_POST(), self.path)
                LocalData.set_record(recordID, data_json)
                self._send_response_with_end_headers(200)
            else:
                self._send_response_with_end_headers(400, 'Bad Request: support only application/json')
        else:
            self._send_response_with_end_headers(403,
                                                 'Bad Request: wrong path, support only "/api/v1/addrecord/*" for posting')
        return

    def do_GET(self):
        """

        :return:
        """
        pattern_for_GET = self.get_pattern_for_GET()
        if re.search(pattern_for_GET, self.path) is not None:
            recordID = self.get_suffix(self.get_path_for_GET(), self.path)
            try:
                record = LocalData.get_record(recordID)
                self._send_response_with_end_headers(200)
                #
                self.wfile.write(record)
            except KeyError:
                self._send_response_with_end_headers(401, "Bad Request: ")
        else:
            self._send_response_with_end_headers(403, "Bad Request: ")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """

    """
    allow_reuse_address = True

    def shutdown(self):
        """

        :return:
        """
        self.socket.close()
        HTTPServer.shutdown(self)


# urls:
# - http://stackoverflow.com/questions/598077/why-does-foo-setter-in-python-not-work-for-me
# - http://stackoverflow.com/a/598090
class SimpleHTTPServer(object):
    """

    """

    class SocketError(SocketServer.socket.error):
        """

        """

        def __init__(self, message, *args):
            """

            :param message:
            :param args:
            :return:
            """
            self.message = message
            super(SimpleHTTPServer.SocketError, self).__init__(message, *args)

    # url: http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python

    class StartError(Exception):
        def __init__(self, message, errors):
            """

            :param message:
            :param errors:
            :return:
            """
            # Call the base class constructor with the parameters it needs
            super(SimpleHTTPServer.StartError, self).__init__(message)

            # Now for your custom code...
            self.errors = errors

    def __init__(self, ip="127.0.0.1", port=8080):
        """

        :param ip:
        :param port:
        :return:
        """
        if isinstance(ip, str) and is_unsigned_integer(port):
            self._ip = ip
            self._port = port
            #
            self.server_thread = None
            self.server = None
            #
            self._thread_name = ""
        else:
            raise ValueError

    # url: http://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters
    @property
    def ip(self):
        """

        :return:
        """
        return self._ip

    @property
    def port(self):
        """

        :return:
        """
        return self._port

    @property
    def thread_name(self):
        """

        :return:
        :rtype: str
        """
        return self._thread_name

    @thread_name.setter
    def thread_name(self, value):
        """

        :param value:
        """
        self._thread_name = value

    def acquire(self, class_handler=HTTPRequestHandler):
        """

        url: http://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use

        :param classHandler:
        """
        try:
            self.server = ThreadedHTTPServer((self.ip, self.port), class_handler)
        except SocketServer.socket.error, e:
            raise SimpleHTTPServer.SocketError(e)

    def start(self, thread_name="httpserver_thread"):
        """

        :return:
        """
        try:
            self._thread_name = thread_name
            self.server_thread = threading.Thread(target=self.server.serve_forever, name=self._thread_name)
            self.server_thread.daemon = True
            self.server_thread.start()
        except Exception, e:
            raise self.StartError("", e)

    def wait_for_thread(self):
        """

        :return:
        """
        self.server_thread.join()

    def stop(self):
        """

        :return:
        """
        self.server.shutdown()
        self.wait_for_thread()


if __name__ == '__main__':
    server = SimpleHTTPServer("127.0.0.1", 8081)
    server.start()
    server.wait_for_thread()
