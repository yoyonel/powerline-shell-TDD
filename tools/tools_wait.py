__author__ = 'latty'

import timeout_decorator  # url: https://pypi.python.org/pypi/timeout-decorator/0.3.2


# url: http://deusyss.developpez.com/tutoriels/Python/args_kwargs/
def wait_for_test_action(test_action, timeout=0.5, **kargs):
    """
    Methode generique pour attendre une action.
    Utilise le decorator 'timeout_decorator'

    :param test_action: Function [->bool] a realiser tant que le retour est vrai
    :type test_action: function
    :param timeout: Temps maximum d'attente pour avoir le bon retour
    :type timeout: float
    :param kargs: Dictionnaire d'arguments a transmettre a 'test_action'
    :type kargs: dict

    :raise TimeoutError: Exception renvoyee si on depasse le timeout pour realiser l'action

    urls:
    - http://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
    -> http://stackoverflow.com/a/24385103
    """
    # use decorator 'timeout_decorator'
    @timeout_decorator.timeout(timeout)
    def _wait_for_action():
        while test_action(**kargs):
            pass

    # call method with decorator
    _wait_for_action()