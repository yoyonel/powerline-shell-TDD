__author__ = 'latty'

from tools.tools_unittest import BaseTest
from tools.tools_network import open_socket_for_listenning, \
    remote_tcp_port_is_free_bash_version, \
    remote_tcp_port_is_free, \
    open_socket_for_listenning_netcat, \
    wait_for_available_port, decorator_wait_for_open_port


class TestToolsNetwork(BaseTest):
    """

    """

    def setUp(self):
        """
        Settings des ip, port pour les tests
        On utilise l'adresse local (localhost='127.0.0.1') et le port 8080

        ps: Il faut verifier (etre sure) que le proxy/firewall de l'OS/routeur/...
        laisse le script de tests communiquer sur cette adressage.
        """
        self.ip = '127.0.0.1'
        self.port = 8081

    @decorator_wait_for_open_port
    def test_open_socket_for_listenning(self):
        """
        Test de la creation d'un object socket

        Utilisation de la lib python: 'socket'
        """
        # On recupere l'object resultant de l'ouverture d'un port pour ecoute
        conn = open_socket_for_listenning(adress=self.ip, port=self.port)
        # On verifie le type de l'objet recupere
        self.assertEqualEllipsis(str(conn), '<socket._socketobject object at 0x...>')
        # On ferme la connexion
        conn.close()

    @decorator_wait_for_open_port
    def test_open_socket_for_listenning_netcat(self):
        """
        Test de la creation d'un processus pour acquisition d'un port par socket.
        Version 'netcat'

        Utilisation de la lib python: 'socket'
        """
        # On recupere le processus lie a l'ouverture d'un port pour ecoute de socket
        process = open_socket_for_listenning_netcat(ip=self.ip, port=self.port)
        # On verifie le type de l'objet recupere
        self.assertEqualEllipsis(str(process), '<subprocess.Popen object at 0x...>')
        # On termine le processus
        process.terminate()

    @decorator_wait_for_open_port
    def test_remote_tcp_port_is_free_netcat(self):
        """
        Test de la fonction qui renvoie l'etat de disponibilite d'un port.

        Utilisation des commandes bash: 'netcat'
        - url: http://www.lestutosdenico.com/tutos-de-nico/netcat
        """
        # On verifie que le port est disponible (libre)
        self.assertTrue(remote_tcp_port_is_free(port=self.port))

        # Ouverture d'une socket en mode listening
        p = open_socket_for_listenning_netcat(self.ip, self.port)
        # On verifie que le port n'est plus libre (acquit)
        self.assertFalse(remote_tcp_port_is_free_bash_version(host=self.ip, port=self.port))
        # On termine le processus netcat => on termine l'acquisition du port
        p.terminate()

        # ############################################################
        # [SYNCH] On attend d'avoir le port cible libre (available)
        wait_for_available_port(self.ip, self.port)
        # ############################################################

        # On verifie que le port est disponible (libre)
        self.assertTrue(remote_tcp_port_is_free_bash_version(host=self.ip, port=self.port))

    @decorator_wait_for_open_port
    def test_remote_tcp_port_is_free(self):
        """
        Test de la fonction qui renvoie l'etat de disponibilite d'un port.

        Utilisation d'une lib python (native): 'socket'
        """
        # On verifie que le port est disponible (libre)
        self.assertTrue(remote_tcp_port_is_free(port=self.port))

        # Ouverture d'une socket en mode listening du port 8080
        conn = open_socket_for_listenning(port=self.port)
        # On verifie que le port n'est plus libre (acquit)
        self.assertFalse(remote_tcp_port_is_free(port=self.port))
        # On ferme la connection (et normalement on libere le port)
        conn.close()
        # On verifie que le port est disponible (libre)
        self.assertTrue(remote_tcp_port_is_free(port=self.port))

        # ############################################################
        # [SYNCH] On attend d'avoir le port cible libre (available)
        wait_for_available_port(self.ip, self.port)
        # ############################################################
