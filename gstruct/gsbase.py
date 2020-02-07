# coding=utf-8

from copy import copy, deepcopy
from functools import partial

from .gsconst import *
from .gsinterface import GSInterface


class GSBase:
    """ The purpose of this class is for producing GStruct object
     with a data structure that matched the definition in itself,
     and keep the registered struct method in it for called use. """

    def __init__(self, struct_definition):
        self._struct_definition = {}
        self._struct_methods = {}

        sdef = dict(struct_definition)
        for sk, sv in sdef.items():
            if isinstance(sv, GSBase):
                for sm_name, _ in sv:
                    if sm_name in self._struct_methods:
                        raise ValueError("Duplicated struct method name!")
                    # Only map the sub method name to the data key
                    self._struct_methods[sm_name] = sk
                continue
            if isinstance(sv, GStruct):
                raise ValueError("The default value of GStruct attribute cannot be type 'GStruct'!")
        self._struct_definition.update(sdef)

    @property
    def struct_definition(self):
        return copy(self._struct_definition)

    def __getitem__(self, item):
        return self._struct_methods[item]

    def __contains__(self, item):
        return item in self._struct_methods

    def __iter__(self):
        return iter(self._struct_methods.items())

    def new(self, data, **options):
        """ Make new object of type 'GStruct' from the defined GSBase object. """
        return GStruct(self, data, **options)

    def def_method(self, method_name, **options):
        """ A decorator that is used to register a struct method function for a
         given method name. """

        def decorator(f):
            if method_name in self:
                raise ValueError("Duplicated GStruct method name!")
            # Map the method name to the real function and its options
            self._struct_methods[method_name] = (f, options,)
            return f

        return decorator

    def make_method_call(self, method_name, gs_obj):
        """ Make a method call function for the specific method name and
         GStruct object. """
        obj = self._struct_methods[method_name]
        if obj is tuple:
            method_func, options = obj
            opt_ref = options.get(OPTION_REF, False)
            return partial(method_func, gs_obj if opt_ref else copy(gs_obj))
        else:
            data_key = obj
            sub_gs_obj = gs_obj.__getattr__(data_key)
            sub_base = sub_gs_obj.gsbase
            return sub_base.make_method_call(method_name, sub_gs_obj)


class GStruct:
    def __init__(self, base, data, **options):
        self._gsbase = base
        if data is None:
            data = {}

        self._struct_data = base.struct_definition
        for sk, sv in self._struct_data.items():
            data_value = data.get(sk)
            if isinstance(sv, GSBase):
                if isinstance(data_value, GStruct):
                    # Accept GStruct object that its GSBase is same with the one in definition
                    if self(data_value):
                        self._struct_data[sk] = data_value
                    else:
                        raise ValueError("Unacceptable GStruct object of data key '{}'!".format(sk))
                elif isinstance(data_value, dict) or data_value is None:
                    # Convert dict object to GStruct object
                    self._struct_data[sk] = sv.new(data_value)
                else:
                    ValueError("Unexpected structure of data key '{}'!".format(sk))
            else:
                self._struct_data[sk] = data_value if data_value is not None else sv

    @property
    def gsbase(self):
        return self._gsbase

    def __call__(self, *args, **kwargs):
        """ Shortcut for type inference of GStruct """
        dest_obj = args[0]
        flag = False
        if isinstance(dest_obj, GStruct):
            flag = self.gsbase == dest_obj.gsbase
        elif isinstance(dest_obj, GSBase):
            gsbase = dest_obj
            flag = self.gsbase == gsbase
        elif isinstance(dest_obj, GSInterface):
            gsinterface = dest_obj
            flag = True
            for i in gsinterface:
                if i not in self.gsbase:
                    flag = False
                    break
        return flag

    def __copy__(self):
        """ Lead copy() to deepcopy() """
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

    def __iter__(self):
        return iter(self._struct_data.items())

    def __contains__(self, item):
        return item in self._struct_data
