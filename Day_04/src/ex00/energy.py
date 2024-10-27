from itertools import zip_longest
from typing import Iterable


def is_str(el):
    return type(el) is str


def all_connect(cable, socket, plug):
    return f'plug {cable} into {socket} using {plug}'


def without_plug(cable, socket):
    return f'weld {cable} to {socket} without plug'


def fix_wiring(cables: Iterable, sockets: Iterable, plugs: Iterable) -> Iterable:
    return [all_connect(c, s, p) if p else without_plug(c, s)
            for c, s, p in zip_longest(
            filter(is_str, cables),
            filter(is_str, sockets),
            filter(is_str, plugs))
            if c and s]


if __name__ == '__main__':
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']

    for c in fix_wiring(cables, sockets, plugs):
        print(c)

    print('----------------------------------------')

    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]

    for c in fix_wiring(cables, sockets, plugs):
        print(c)
