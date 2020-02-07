# coding=utf-8


class GSInterface:
    def __init__(self, interface_list=None):
        if interface_list is None:
            interface_list = []

        self._interface_list = interface_list
        self._gsref = None

    def __iter__(self):
        return iter(list(self._interface_list))
