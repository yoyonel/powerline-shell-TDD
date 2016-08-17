__author__ = 'latty'

import re
import unittest


class BaseTest(unittest.TestCase):
    """
    url: https://gist.github.com/harobed/5845674
    """

    def assertEqualEllipsis(self, first, second, ellipsis_marker='...', msg=None):
        """


        :param first:
        :param second:
        :param ellipsis_marker:
        :type ellipsis_marker: str
        :param msg:
        # Example :
        #     >>> self.assertEqualEllipsis('foo123bar', 'foo...bar')
        """
        if ellipsis_marker not in second:
            return first == second

        re_found = re.match(re.escape(second).replace(re.escape(ellipsis_marker), '(.*?)'),
                            first,
                            re.M | re.S)

        if re_found is None:
            self.assertMultiLineEqual(first,
                                      second,
                                      msg)