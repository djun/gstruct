# coding=utf-8

from copy import copy
from functools import partial


class GStruct:

    def __init__(self, struct_definition):
        self._struct_base = dict(struct_definition)
        self._struct_methods = {}

    def __len__(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __missing__(self, key):
        pass

    def call(self):
        pass

    def ref_call(self):
        pass
