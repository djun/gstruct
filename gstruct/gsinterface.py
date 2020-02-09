# coding=utf-8

import importlib


class GSInterface:
    """ The purpose of this class is for simply building up a filter
    contained a set of method names, and keep a set cached
    the matched GStruct objects. """

    def __init__(self, interfaces=None):
        if interfaces is None:
            interfaces = set()
        if type(interfaces) in {list, tuple}:
            interfaces = set(interfaces)
        if not isinstance(interfaces, set):
            raise ValueError("Interface cannot be type {}!".format(type(interfaces)))

        self.__dict__['__interfaces'] = interfaces
        self.__dict__['__cached_struct_set'] = set()

    @property
    def interfaces_(self):
        return set(self.__dict__['__interfaces'])

    def __iter__(self):
        return iter(set(self.interfaces_))

    def __mul__(self, other):
        """ Shortcut for self.wrap(gs_obj) """
        return self.wrap(other)

    def match(self, gsbase):
        if not gsbase.__class__.__name__ == "GSBase":
            raise ValueError("Can only accept object type 'GSBase'!")

        if id(gsbase) in self.__dict__['__cached_struct_set']:
            flag = True
        else:
            flag = True
            for i in self.__dict__['__interfaces']:
                if i not in gsbase:
                    flag = False
                    break
            if flag:
                self.__dict__['__cached_struct_set'].add(id(gsbase))

        return flag

    def wrap(self, gs_obj):
        return GSIWrapper(self, gs_obj)


class GSIWrapper:
    """ This class can wrap a GSObject matched the right GSInterface. """

    def __init__(self, gsi_object, gs_obj):
        if not isinstance(gsi_object, GSInterface):
            raise ValueError("'gsi_object' can only accept object type 'GSInterface'!")
        if not gs_obj.__class__.__name__ == "GStruct":
            raise ValueError("'gs_obj' can only accept object type 'GStruct'!")

        if gsi_object.match(gs_obj.gsbase_):
            self.__dict__['__wrapped_obj'] = gs_obj
            self.__dict__['__interfaces'] = gsi_object.interfaces_
        else:
            raise ValueError("Cannot wrap a GStruct object not matched as a GSIWrapper!")

    def __getattr__(self, item):
        if item in self.__dict__['__interfaces']:
            return getattr(self.__dict__['__wrapped_obj'], item)
        else:
            raise AttributeError("Has no interface '{}'!".format(item))
