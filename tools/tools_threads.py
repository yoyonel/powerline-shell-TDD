__author__ = 'latty'

import threading


def find_active_thread(name):
    """
    urls:
    - stackoverflow.com/questions/9868653/find-first-list-item-that-matches-criteria
    - https://docs.python.org/2/library/threading.html#threading.enumerate

    :param name:
    :type name: str
    :return:
    :rtype: Thread

    """
    try:
        list_actives_threads = threading.enumerate()
        return next(thread for thread in list_actives_threads if thread.getName() == name)
    except StopIteration:
        return None


def is_thread_alive(name):
    """

    :param name:
    :type name: str
    :return:
    :rtype: bool

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
    :type name: str
    :return:
    :rtype: bool
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