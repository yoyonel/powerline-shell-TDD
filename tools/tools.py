__author__ = 'atty'

import subprocess
import threading
import requests


def execute_cmd(cmd, default=""):
    """

    :param cmd:
    :param default:
    :return:

    >>> execute_cmd("") #doctest: +ELLIPSIS
    ('', <subprocess.Popen object at 0x...>)
    >>> execute_cmd("", "test") #doctest: +ELLIPSIS
    ('', <subprocess.Popen object at 0x...>)
    >>> execute_cmd("printf test") #doctest: +ELLIPSIS
    ('test', <subprocess.Popen object at 0x...>)
    """
    output = default
    bashprocess = None
    # url: http://stackoverflow.com/a/13333130
    try:
        bashprocess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # url: http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
        output = bashprocess.communicate()[0].rstrip("\n")
    except Exception as e:
        raise e
    finally:
        return output, bashprocess


def execute_cmd_noresult(cmd, default=""):
    """
    Meme comportement que 'execute_cmd' mais n'attend pas le retour de la commande.
    Cela permet de lancer une commande shell en background (sans etre bloque par le retour d'une valeur).

    :param cmd: str
    :param default: str
    :return: subprocess.Popen object

    >>> execute_cmd_noresult("") #doctest: +ELLIPSIS
    <subprocess.Popen object at 0x...>
    >>> execute_cmd_noresult("", "test") #doctest: +ELLIPSIS
    <subprocess.Popen object at 0x...>
    >>> execute_cmd_noresult("printf test") #doctest: +ELLIPSIS
    <subprocess.Popen object at 0x...>
    """
    bashprocess = None
    # url: http://stackoverflow.com/a/13333130
    try:
        bashprocess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        raise e
    finally:
        return bashprocess


def remote_tcp_port_is_open(host='localhost', port=8080):
    """
    urls:
    - http://stackoverflow.com/questions/9609130/quick-way-to-find-if-a-port-is-open-on-linux
    - http://stackoverflow.com/questions/4922943/test-from-shell-script-if-remote-tcp-port-is-open

    :param host:
    :param port:
    :return:

    >>> # url: http://www.lestutosdenico.com/tutos-de-nico/netcat
    >>> p = execute_cmd_noresult("nc -l -p 8081")
    >>> remote_tcp_port_is_open(host='127.0.0.1', port=8081)
    False
    >>> p.terminate()
    >>> remote_tcp_port_is_open(host='127.0.0.1', port=8081)
    True
    """
    cmd = "nc -z {} {}; echo $?".format(host, port)
    result, _ = execute_cmd(cmd, "1")
    return bool(int(result))


def is_unsigned_integer(value):
    """

    :param value:
    :return:

    >>> is_unsigned_integer(0)
    True
    >>> is_unsigned_integer(65535)
    True
    >>> is_unsigned_integer(-1)
    False
    >>> is_unsigned_integer(65536)
    False
    >>> is_unsigned_integer('0')
    False
    >>> is_unsigned_integer(0.0)
    False
    """
    return isinstance(value, int) and (value >= 0) and (value.bit_length() <= 16)


def find_active_thread(name):
    """
    urls:
    - stackoverflow.com/questions/9868653/find-first-list-item-that-matches-criteria
    - https://docs.python.org/2/library/threading.html#threading.enumerate

    :param name:
    :return:

    >>> # urls:
    >>> # - http://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
    >>> # -> http://stackoverflow.com/a/36499538
    >>> find_active_thread("__unittest_find_active_thread__")
    >>> import threading
    >>> def doit(stop_event, _):
    ...     while not stop_event.wait(1):
    ...         pass
    >>> pill2kill = threading.Event()
    >>> t = threading.Thread(target=doit, name="__unittest_find_active_thread__", args=(pill2kill, None))
    >>> t.start()
    >>> find_active_thread("__unittest_find_active_thread__") #doctest: +ELLIPSIS
    <Thread(__unittest_find_active_thread__, started ...)>
    >>> pill2kill.set()
    >>> t.join()
    >>> find_active_thread("__unittest_find_active_thread__")

    """
    try:
        list_actives_threads = threading.enumerate()
        return next(thread for thread in list_actives_threads if thread.getName() == name)
    except StopIteration:
        return None


def is_thread_alive(name):
    """

    :param name:
    :return:

    >>> is_thread_alive("__unittest_find_active_thread__")
    False
    >>> import threading
    >>> def doit(stop_event, _):
    ...     while not stop_event.wait(1):
    ...         pass
    >>> pill2kill = threading.Event()
    >>> t = threading.Thread(target=doit, name="__unittest_find_active_thread__", args=(pill2kill, None))
    >>> t.start()
    >>> is_thread_alive("__unittest_find_active_thread__")
    True
    >>> pill2kill.set()
    >>> t.join()
    >>> is_thread_alive("__unittest_find_active_thread__")
    False
    """
    result = False
    try:
        searched_thread = find_active_thread(name)
        result = searched_thread.isAlive()
    except StopIteration:
        pass
    except AttributeError:
        pass
    finally:
        return result


def is_thread_daemon(name):
    """

    :param name:
    :return:

    >>> is_thread_daemon("__unittest_find_active_thread__")
    False
    >>> import threading
    >>> def doit(stop_event, _):
    ...     while not stop_event.wait(1):
    ...         pass
    >>> pill2kill = threading.Event()
    >>> t = threading.Thread(target=doit, name="__unittest_find_active_thread__", args=(pill2kill, None))
    >>> t.daemon = True
    >>> t.start()
    >>> is_thread_daemon("__unittest_find_active_thread__") #doctest: +ELLIPSIS
    True
    >>> pill2kill.set()
    >>> t.join()
    >>> is_thread_daemon("__unittest_find_active_thread__")
    False
    """
    result = False
    try:
        searched_thread = find_active_thread(name)
        result = searched_thread.isDaemon()
    except StopIteration:
        pass
    except AttributeError:
        pass
    finally:
        return result


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

    >>> ip='127.0.0.1'; port=8081; code_result = 201
    >>> remote_tcp_port_is_open(host=ip, port=port)
    True
    >>> # url: http://stackoverflow.com/questions/16640054/minimal-web-server-using-netcat
    >>> bash_cmds_for_dummy_httpserver = "while true; do { echo 'HTTP/1.1 %d OK\\n\\r';}| nc -l %s %d; done" % (code_result, ip, port)
    >>> p = execute_cmd_noresult(bash_cmds_for_dummy_httpserver)
    >>> while not remote_tcp_port_is_open(host=ip, port=port):  # temporisation pour acquerir l'ip/port avec nc
    ...     pass
    >>> perform_GET_request(ip, port)
    <Response [201]>
    >>> p.terminate()
    >>> while not remote_tcp_port_is_open(host=ip, port=port):  # temporisation pour liberer l'ip/port avec nc
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

    >>> ip='127.0.0.1'; port=8081; code_result = 202
    >>> remote_tcp_port_is_open(host=ip, port=port)
    True
    >>> bash_cmds_for_dummy_httpserver = "while true; do { echo 'HTTP/1.1 %d OK\\n\\r';}| nc -l %s %d; done" % (code_result, ip, port)
    >>> p = execute_cmd_noresult(bash_cmds_for_dummy_httpserver)
    >>> while not remote_tcp_port_is_open(host=ip, port=port):  # temporisation pour acquerir l'ip/port avec nc
    ...     pass
    >>> perform_POST_request(ip, port)
    <Response [202]>
    >>> p.terminate()
    >>> while not remote_tcp_port_is_open(host=ip, port=port):  # temporisation pour liberer l'ip/port avec nc
    ...     pass
    """
    return requests.post(build_url(ip, port, path), data=data, json=json)