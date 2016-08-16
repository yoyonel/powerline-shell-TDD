# coding=utf-8
__author__ = 'atty'

import unittest
from app.http_server import SimpleHTTPServer, HTTPRequestHandler, LocalData
from tools.tools import remote_tcp_port_is_open, \
    is_thread_alive, is_thread_daemon, \
    perform_GET_request, perform_POST_request, \
    get_dict_from_get_response
import SocketServer


# [TODO]: Docs/urls à lire
# - https://pythonhosted.org/tl.testing/tl.testing-thread.html
# - http://nose.readthedocs.io/en/latest/usage.html
# - https://www.amazon.com/Testing-Python-Applying-Unit-Acceptance/dp/1118901223
# -> https://github.com/florije1988/Python_Testing/blob/master/Wiley.Testing%20Python%20Applying%20Unit%20Testing,%20TDD,%20BDD%20and%20Acceptance%20Testing.(2014).pdf
# - http://code.tutsplus.com/tutorials/beginning-test-driven-development-in-python--net-30137
# - https://docs.python.org/2/library/unittest.html

class Test_HTTPServer(unittest.TestCase):
    """

    """

    def setUp(self):
        """
        Faut faire attention !
        Faut etre sure de choisr une adresse+port deja libre !
        Ou sinon faudrait faire aussi un test unitaire la dessus ... a voir ;-)
        :return:
        """
        self.ip = "127.0.0.1"
        self.port = 8081  # 8081 car 8080 potentiellement utilise par le serveur http de PowerLine-Shell
        #
        self.access_to_post_handler = False
        self.access_to_get_handler = False

    def test_httpserver_getter_setter(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        # #######################################################################
        self.assertEqual(http_server.ip, self.ip)
        self.assertEqual(http_server.port, self.port)
        ########################################################################

    def test_httpserver_acquire_ip_port(self):
        """

        :return:
        """

        #
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()
        ########################################################################
        self.assertEqual(remote_tcp_port_is_open(http_server.ip, http_server.port), False)
        ########################################################################

    def test_httpserver_return_error_if_adress_if_already_bind(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()

        http_server_2 = SimpleHTTPServer(ip=self.ip, port=self.port)
        ########################################################################
        self.assertRaises(SocketServer.socket.error, http_server_2.acquire)
        self.assertRaises(SimpleHTTPServer.SocketError, http_server_2.acquire)
        ########################################################################

    def test_httpserver_return_error_if_adress_if_wrong(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer("wrong ip", port=self.port)
        ########################################################################
        self.assertRaises(SocketServer.socket.error, http_server.acquire)
        self.assertRaises(SimpleHTTPServer.SocketError, http_server.acquire)
        ########################################################################

    def test_httpserver_return_error_if_arguments_if_wrong_types(self):
        """

        :return:
        """
        ########################################################################
        # ip
        self.assertRaises(ValueError, SimpleHTTPServer, 1, self.port)
        # port
        self.assertRaises(ValueError, SimpleHTTPServer, self.ip, "8080")
        self.assertRaises(ValueError, SimpleHTTPServer, self.ip, 8080.0)
        self.assertRaises(ValueError, SimpleHTTPServer, self.ip, -1)
        self.assertRaises(ValueError, SimpleHTTPServer, self.ip, 65535 + 1)
        ########################################################################

    def test_httpserver_start(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()
        http_server.start(thread_name="test_httpserver_thread")

        ########################################################################
        # on test si le thread utilise par le server http
        # est lance et utilise en mode daemon
        self.assertEqual(is_thread_alive(http_server.thread_name), True)
        self.assertEqual(is_thread_daemon(http_server.thread_name), True)
        ########################################################################

        http_server.stop()

    def test_httpserver_return_error_if_start_before_acquire(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        ########################################################################
        self.assertRaises(SimpleHTTPServer.StartError, http_server.start)
        ########################################################################

    class Test_HTTPRequestHandler(HTTPRequestHandler):
        """
        Tests par heritage de la classe (a tester): HTTPRequestHandler
         On overload la methode callback sur l'event: GET
         On ne le fait que pour GET car le GET ne permet d'enregistrer de valeurs
         (donc pas possible de tester une valeur).
        """

        def do_GET(self):
            """

            """
            super(Test_HTTPServer.Test_HTTPRequestHandler, self).do_GET()
            #
            LocalData._records['access_to_get'] = None

    def test_httpserver_class_handler_access_to_get_callback(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire(self.Test_HTTPRequestHandler)
        http_server.start()

        # requete GET
        perform_GET_request(self.ip, self.port)

        http_server.stop()

        # #######################################################################
        self.assertEqual('access_to_get' in LocalData._records, True)
        ########################################################################

    def test_httpserver_class_handler_access_to_post_callback(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()
        http_server.start()

        # requete POST
        path_suffix_for_test = 'unittest'
        path = HTTPRequestHandler.get_path_for_POST() + path_suffix_for_test
        json = {}
        response = perform_POST_request(self.ip,
                                        self.port,
                                        path=path,
                                        json=json)

        http_server.stop()

        ########################################################################
        self.assertEqual(response.status_code, 200)  # status_code == OK
        self.assertEqual(path_suffix_for_test in LocalData._records, True)
        ########################################################################

    def test_httpserver_class_handler_post_json_values(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()
        http_server.start()

        # requete POST
        path_suffix_for_test = 'unittest'
        path = HTTPRequestHandler.get_path_for_POST() + path_suffix_for_test
        json = {"test": 123}
        response = perform_POST_request(self.ip,
                                        self.port,
                                        path=path,
                                        json=json)

        http_server.stop()

        ########################################################################
        self.assertEqual(response.status_code, 200)  # status_code == OK
        self.assertEqual(path_suffix_for_test in LocalData._records, True)
        self.assertEqual(LocalData._records[path_suffix_for_test], json)
        ########################################################################

    def test_httpserver_class_handler_get_json_values(self):
        """

        :return:
        """
        http_server = SimpleHTTPServer(ip=self.ip, port=self.port)
        http_server.acquire()
        http_server.start()

        # requete POST
        path_suffix_for_test = '__unittest_test_httpserver_class_handler_get_json_values__'
        path_for_POST = HTTPRequestHandler.get_path_for_POST() + path_suffix_for_test
        json = {path_suffix_for_test: path_suffix_for_test}
        perform_POST_request(self.ip,
                             self.port,
                             path=path_for_POST,
                             json=json)

        path_for_GET = HTTPRequestHandler.get_path_for_GET() + path_suffix_for_test
        get_response = perform_GET_request(self.ip,
                                           self.port,
                                           path=path_for_GET)

        # #######################################################################
        self.assertEqual(get_response.status_code, 200)  # status_code == OK
        ########################################################################

        http_server.stop()

        ########################################################################
        self.assertNotEqual(get_response.content, '')  # A t'on recupere une reponse ?
        ########################################################################

        dict_json_from_get_request = get_dict_from_get_response(get_response)

        ########################################################################
        self.assertEqual(dict_json_from_get_request, json)  # la reponse est celle attendue (celle envoyee)
        ########################################################################

if __name__ == '__main__':
    unittest.main()
