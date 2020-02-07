# coding=utf-8


class GSInterface:
    """ The purpose of this class is for simply building up a filter
    contained a list of method names. It only do one thing that
    keeping the list , so far. """

    def __init__(self, interface_list=None):
        if interface_list is None:
            interface_list = []

        self._interface_list = interface_list

    def __iter__(self):
        return iter(list(self._interface_list))
