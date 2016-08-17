__author__ = 'latty'

import ast
import requests
from tools_shell import execute_cmd_noresult
from tools_network import remote_tcp_port_is_free_bash_version


def build_url(ip, port, path=""):
    """

    :param ip:
    :param port:
    :param path:
    :return:

    >>> build_url("localhost", 8080)
    'http://localhost:8080/'
    >>> build_url("localhost", 8080, 'api/v1/apprecord')
    'http://localhost:8080/api/v1/apprecord'
    """
    return "http://{}:{}/{}".format(ip, port, path)


def perform_GET_request(ip, port, path=""):
    """

    :param ip:
    :param port:
    :param path:
    :return:

    >>> ip='127.0.0.1'; port=8080; code_result = 201
    >>> remote_tcp_port_is_free_bash_version(host=ip, port=port)
    True
    >>> # url: http://stackoverflow.com/questions/16640054/minimal-web-server-using-netcat
    >>> bash_cmds_for_dummy_httpserver = "while true; do { echo 'HTTP/1.1 %d OK\\n\\r';}| nc -l %s %d; done" % (code_result, ip, port)
    >>> p = execute_cmd_noresult(bash_cmds_for_dummy_httpserver)
    >>> while not remote_tcp_port_is_free_bash_version(host=ip, port=port):  # temporisation pour acquerir l'ip/port avec nc
    ...     pass
    >>> perform_GET_request(ip, port)
    <Response [201]>
    >>> p.terminate()
    >>> while not remote_tcp_port_is_free_bash_version(host=ip, port=port):  # temporisation pour liberer l'ip/port avec nc
    ...     pass
    """
    return requests.get(build_url(ip, port, path))


def perform_POST_request(ip, port, path="", data=None, json=None):
    """

    :param ip:
    :param port:
    :param path:
    :param data:
    :param json:
    :return:

    >>> ip='127.0.0.1'; port=8080; code_result = 202
    >>> remote_tcp_port_is_free_bash_version(host=ip, port=port)
    True
    >>> bash_cmds_for_dummy_httpserver = "while true; do { echo 'HTTP/1.1 %d OK\\n\\r';}| nc -l %s %d; done" % (code_result, ip, port)
    >>> p = execute_cmd_noresult(bash_cmds_for_dummy_httpserver)
    >>> while not remote_tcp_port_is_free_bash_version(host=ip, port=port):  # temporisation pour acquerir l'ip/port avec nc
    ...     pass
    >>> perform_POST_request(ip, port)
    <Response [202]>
    >>> p.terminate()
    >>> while not remote_tcp_port_is_free_bash_version(host=ip, port=port):  # temporisation pour liberer l'ip/port avec nc
    ...     pass
    """
    return requests.post(build_url(ip, port, path), data=data, json=json)


def get_dict_from_get_response(get_response):
    """

    :param get_response:
    :return:
    """
    return ast.literal_eval(get_response.content)