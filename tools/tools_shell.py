__author__ = 'latty'

import subprocess


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