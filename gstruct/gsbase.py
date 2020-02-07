# coding=utf-8

from copy import copy, deepcopy
from functools import partial

from .gsconst import *
from .gsinterface import GSInterface


class GSBase:
    def __init__(self, struct_definition):
        self._struct_definition = {}
        self._struct_methods = {}
        self._struct_sub_base = {}

        sdef = dict(struct_definition)
        for sk, sv in sdef.items():
            if isinstance(sv, GSBase):
                self._struct_sub_base[sk] = sv
                # TODO self._struct_methods
                continue
            if isinstance(sv, GStruct):
                raise ValueError("The default value of GStruct attribute cannot be type 'GStruct'!")
        self._struct_definition.update(sdef)

    @property
    def struct_definition(self):
        return copy(self._struct_definition)

    def __getitem__(self, item):
        # TODO
        pass

    def __contains__(self, item):
        # TODO
        flag = item in self._struct_methods
        if not flag:
            for sb in self._struct_sub_base.values():
                flag = item in sb
                if flag:
                    break
        return flag

    def new(self, data, **options):
        """ Make new object of type 'GStruct' from the defined GSBase object. """
        return GStruct(self, data, **options)

    def def_method(self, method_name, **options):
        """ A decorator that is used to register a struct method function for a
        given method name. """

        def decorator(f):
            if method_name in self:
                raise RuntimeError("Duplicated struct method name!")
            self._struct_methods[method_name] = (f, options,)
            return f

        return decorator

    def make_method_call(self, method_name, gs_obj):
        # TODO
        method_func, options = self._struct_methods[method_name]
        opt_ref = options.get(OPTION_REF, False)
        return partial(method_func, gs_obj if opt_ref else copy(gs_obj))


class GStruct:
    def __init__(self, base, data, **options):
        # TODO data: sub dict -> gstruct obj
        self._gsbase = base
        self._struct_data = {}

    @property
    def gsbase(self):
        return self._gsbase

    def __call__(self, *args):
        """ Shortcut for type inference of GStruct """
        dest_obj = args[0]
        flag = False
        if isinstance(dest_obj, GStruct):
            flag = self.gsbase == dest_obj.gsbase
        elif isinstance(dest_obj, GSInterface):
            # TODO
            pass
        return flag

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        new_data = {}
        for sk, sv in self._struct_data.items():
            new_data[sk] = deepcopy(sv, memodict)
        new_obj = self.__class__(self._gsbase, new_data)
        memodict[id(new_obj)] = new_obj
        return new_obj

    def __getattr__(self, item):
        """ Shortcut for get attribute value or method of this GStruct object """
        if item in self._struct_data:
            return self._struct_data[item]
        elif item in self._gsbase:
            return self._gsbase.make_method_call(item, self)
        else:
            return None

    def __setattr__(self, key, value):
        """ Shortcut for set attribute value of this GStruct object (NOT for GStruct method) """
        self._struct_data[key] = value

    def __len__(self):
        return len(self._struct_data)

    def __getitem__(self, item):
        return self.make_call(item)

    def __iter__(self):
        # TODO
        raise RuntimeError("Iteration not supported!")

    def __contains__(self, item):
        return item in self._gsbase
