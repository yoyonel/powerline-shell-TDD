__author__ = 'atty'


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
