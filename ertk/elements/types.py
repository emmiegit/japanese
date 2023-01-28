from collections import namedtuple
from typing import Union

Name = str
Multiplied = namedtuple('Multiplied', ('count', 'expression'))
HorizontalList = namedtuple('HorizontalList', ('items'))
VerticalList = namedtuple('VerticalList', ('items'))

Expression = Union[Name, Multiplied, HorizontalList, VerticalList]

def flatten(list_class, first, second):
    if type(first) == list_class and type(second) == Name:
        return list_class(first.items + [second])
    elif type(second) == list_class and type(first) == Name:
        return list_class([first] + second.items)
    else:
        return list_class([first, second])
