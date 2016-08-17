__author__ = 'latty'

import socket
from contextlib import closing
from tools_shell import execute_cmd, execute_cmd_noresult
from tools_wait import wait_for_test_action
from functools import wraps


def wait_for_available_port(ip, port, timeout=0.5):
    """

    :param ip:
    :param port:
    :param timeout:
    :return:
    """

    def action_wait_for_avalaible_port(_ip, _port):
        return not remote_tcp_port_is_free_bash_version(_ip, _port)

    #
    wait_for_test_action(action_wait_for_avalaible_port, timeout, _ip=ip, _port=port)


def decorator_wait_for_open_port(method, timeout=0.5):
    """
    Decorateur pour encapsuler une methode/fonction par une attente synchrone
    sur l'accessibilite d'un port (sur ip).
    Ce decorateur est particulierement util pour la synchronisation des tests (unitaires).

    urls:
    - http://stackoverflow.com/questions/11731136/python-class-method-decorator-w-self-arguments
    -> http://stackoverflow.com/a/36944992

    :param method:
    :type method: function
    :param timeout:
    :type timeout: float
    """

    @wraps(method)
    def _impl(self, *args, **kwargs):
        wait_for_available_port(self.ip, self.port, timeout)
        method(self, *args, **kwargs)
        wait_for_available_port(self.ip, self.port, timeout)
        pass

    return _impl


def open_socket_for_listenning(adress_family=socket.AF_INET,
                               socket_type=socket.SOCK_STREAM,
                               adress='', port=8080,
                               max_nb_clients_for_listenning=1):
    """

    :param adress_family:
    :type adress_family: integer
    :param socket_type:
    :type socket_type: integer
    :param adress:
    :type adress: string
    :param port:
    :type port: integer
    :param max_nb_clients_for_listenning:
    :type max_nb_clients_for_listenning: integer
    :return:
    :rtype: _socketobject

    """
    # construction de la socket
    connexion = socket.socket(adress_family, socket_type)
    # connexion de la socket
    connexion.bind((adress, port))
    #
    connexion.listen(max_nb_clients_for_listenning)

    return connexion


def open_socket_for_listenning_netcat(ip, port):
    """

    :param ip:
    :type ip: str
    :param port:
    :type port: integer
    :return:
    """
    # Ouverture d'une socket en mode listening
    p = execute_cmd_noresult("nc -l -p {} {}".format(port, ip))
    return p


def remote_tcp_port_is_free_bash_version(host='localhost', port=8080):
    """
    urls:
    - http://stackoverflow.com/questions/9609130/quick-way-to-find-if-a-port-is-open-on-linux
    - http://stackoverflow.com/questions/4922943/test-from-shell-script-if-remote-tcp-port-is-open

    :param host:
    :type host: str
    :param port:
    :type port: integer
    :return:
    :rtype: bool

    """
    cmd = "nc -z {} {}; echo $?".format(host, port)
    result, _ = execute_cmd(cmd, "1")
    return bool(int(result))


def remote_tcp_port_is_free(host='localhost', port=8080, timeout=1):
    """

    :param host:
    :param port:
    :param timeout:
    :return:

    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)  # set Timeout
        return sock.connect_ex((host, port)) is not 0

