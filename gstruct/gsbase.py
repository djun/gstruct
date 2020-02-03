# coding=utf-8

from copy import copy
from functools import partial

from .gsinterface import GSInterface


class GSBase:
    def __init__(self, struct_definition):
        self._struct_definition = dict(struct_definition)
        self._struct_methods = {}

    def __setitem__(self, key, value):
        # TODO
        pass

    def __delitem__(self, key):
        # TODO
        pass

    def __iter__(self):
        raise RuntimeError("Iteration not supported!")

    def __contains__(self, item):
        return item in self._struct_methods

    def __missing__(self, key):
        raise RuntimeError("Struct method not found!")

    def new(self, data, make_copy=True):
        # self.__class__
        pass

    def append(self, method_):
        pass

    def make_call(self, struct_data, method_name, ref_call=False):
        method_, spath, gsbase = self._struct_methods[method_name]
        # TODO spath, struct_data
        return partial(method_, gsbase.new(spath, make_copy=not ref_call))

    def make_ref_call(self, struct_data, method_name):
        self.make_call(struct_data, method_name, ref_call=True)


class GStruct:
    def __init__(self, base, data):
        # TODO data
        self._gsbase = base
        self._struct_data = {}

    def __getattr__(self, item):
        return self._struct_data[item]

    def __setattr__(self, key, value):
        self._struct_data[key] = value

    def __len__(self):
        return len(self._struct_data)

    def __getitem__(self, item):
        return self.make_call(item)

    def __setitem__(self, key, value):
        raise RuntimeError("Read-only struct methods!")

    def __delitem__(self, key):
        raise RuntimeError("Read-only struct methods!")

    def __iter__(self):
        raise RuntimeError("Iteration not supported!")

    def __contains__(self, item):
        return item in self._gsbase

    def __missing__(self, key):
        raise RuntimeError("Struct method not found!")

    def __call__(self, *args, **kwargs):
        item = args[0]
        if isinstance(item, GSInterface):
            gsinterface = item
            # TODO

    def make_call(self, method_name, ref_call=False):
        # TODO
        return self._gsbase.make_call(self._struct_data, method_name, ref_call=ref_call)

    def make_ref_call(self, method_name):
        # TODO
        return self._gsbase.make_call(self._struct_data, method_name, ref_call=True)
