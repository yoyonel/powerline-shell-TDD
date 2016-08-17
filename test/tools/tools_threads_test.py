from tools.tools_threads import find_active_thread, is_thread_alive

__author__ = 'latty'

from tools.tools_unittest import BaseTest
import threading


class TestToolsThreads(BaseTest):
    """

    """

    def setUp(self):
        """

        """
        pass

    def test_find_active_thread(self):
        """
        urls:
        - http://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
        -> http://stackoverflow.com/a/36499538

        :return:
        """
        thread_name = "__unittest_find_active_thread__"

        self.assertIsNone(find_active_thread(thread_name))

        def _worker_thread_wait(stop_event, _):
            while not stop_event.wait(1):
                pass

        pill2kill = threading.Event()
        t = threading.Thread(target=_worker_thread_wait,
                             name=thread_name,
                             args=(pill2kill, None))
        t.start()

        self.assertEqualEllipsis(str(find_active_thread(thread_name)),
                                 '<Thread({}, started ...)>'.format(thread_name))

        pill2kill.set()
        t.join()

        self.assertIsNone(find_active_thread(thread_name))

    def test_is_thread_alive(self):
        """
        
        :return:
        """
        thread_name = "__unittest_is_thread_alive__"

        self.assertFalse(is_thread_alive(thread_name))

        def _worker_thread_wait(stop_event, _):
            while not stop_event.wait(1):
                pass

        pill2kill = threading.Event()
        t = threading.Thread(target=_worker_thread_wait,
                             name=thread_name,
                             args=(pill2kill, None))
        t.start()

        self.assertTrue(is_thread_alive(thread_name))

        pill2kill.set()
        t.join()

        self.assertFalse(is_thread_alive(thread_name))

    def test_is_thread_daemon(self):
        """

        :return:
        """
        thread_name = "__unittest_is_thread_daemon__"

        self.assertFalse(is_thread_alive(thread_name))

        def _worker_thread_wait(stop_event, _):
            while not stop_event.wait(1):
                pass

        pill2kill = threading.Event()
        t = threading.Thread(target=_worker_thread_wait,
                             name=thread_name,
                             args=(pill2kill, None))
        t.start()

        self.assertTrue(is_thread_alive(thread_name))

        pill2kill.set()
        t.join()

        self.assertFalse(is_thread_alive(thread_name))