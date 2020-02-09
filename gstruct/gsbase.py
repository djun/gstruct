# coding=utf-8

import traceback as tb
from copy import copy, deepcopy
from functools import partial

from .gsconst import *
from .gsinterface import GSInterface


class GSBase:
    """ The purpose of this class is for producing GStruct object
     with a data structure that matched the definition in itself,
     and keep the registered struct method in it for called use. """

    def __init__(self, struct_definition):
        # TODO Buggy!
        # st = tb.extract_stack()
        # filename, line_number, function_name, text = st[-2]
        # self.__dict__['__struct_base_name'] = text[:text.find('=')].strip()

        self.__dict__['__struct_definition'] = {}
        self.__dict__['__struct_methods'] = {}

        sdef = dict(struct_definition)
        for sk, sv in sdef.items():
            if isinstance(sv, GSBase):
                for sm_name, _ in sv:
                    if sm_name in self.__dict__['__struct_methods']:
                        raise ValueError("Duplicated struct method name!")
                    # Only map the sub method name to the data key
                    self.__dict__['__struct_methods'][sm_name] = sk
                continue
            if isinstance(sv, GStruct):
                raise ValueError("The default value of GStruct attribute cannot be type 'GStruct'!")
        self.__dict__['__struct_definition'].update(sdef)

    @property
    def name_(self):
        return self.__dict__['__struct_base_name']

    @property
    def struct_definition_(self):
        return copy(self.__dict__['__struct_definition'])

    def __getitem__(self, item):
        return self.__dict__['__struct_methods'][item]

    def __contains__(self, item):
        return item in self.__dict__['__struct_methods']

    def __iter__(self):
        return iter(self.__dict__['__struct_methods'].items())

    # def __add__(self, other):  # TODO Buggy!
    #     """ Shortcut for composing two GSBase objects, or
    #     composing one GSBase object and one dict object,
    #     to a new GSBase object. """
    #
    #     st = {
    #         self.name_: self,
    #     }
    #     st2 = other
    #     if isinstance(st2, GSBase):
    #         st.update({
    #             st2.name_: st2,
    #         })
    #     elif isinstance(st2, dict):
    #         st.update(st2)
    #     else:
    #         raise TypeError(
    #             "GSBase cannot be composed with this type {}, except 'GSBase' and 'dict'!".format(type(other)))
    #     return self.__class__(st)

    def __mul__(self, other):
        """ Shortcut for self.new(data=data) """
        return self.new(data=other)

    def new(self, data=None, **options):
        """ Make new object of type 'GStruct' from the defined GSBase object. """
        return GStruct(self, data, **options)

    def def_method(self, method_name=None, **options):
        """ A decorator that is used to register a struct method function for a
         given method name. """

        def decorator(f):
            mn = method_name if method_name is not None else f.__name__
            if mn in self:
                obj = self.__dict__['__struct_methods'][mn]
                if isinstance(obj, tuple):
                    # Allow override methods of sub GSBase, but not in the same GSBase
                    raise ValueError("Duplicated method name in GSBase!")
            # Map the method name to the real function and its options
            self.__dict__['__struct_methods'][mn] = (f, options,)
            return f

        return decorator

    def make_method_call(self, method_name, gs_obj):
        """ Make a method call function for the specific method name and
         GStruct object. """
        obj = self.__dict__['__struct_methods'][method_name]
        if isinstance(obj, tuple):
            method_func, options = obj
            opt_ref = options.get(OPTION_REF, False)
            return partial(method_func, gs_obj if opt_ref else copy(gs_obj))
        elif isinstance(obj, str):
            data_key = obj
            sub_gs_obj = getattr(gs_obj, data_key)
            sub_base = sub_gs_obj.gsbase_
            return sub_base.make_method_call(method_name, sub_gs_obj)
        else:
            raise ValueError("Unexpected method name!")


class GStruct:
    """ This class can be regarded as 'the instance of GSBase',
    and its real instance store the actual data in it. """

    def __init__(self, base, data, **options):
        self.__dict__['__gsbase'] = base
        if data is None:
            data = {}

        self.__dict__['__struct_data'] = base.struct_definition_
        for sk, sv in self.__dict__['__struct_data'].items():
            data_value = data.get(sk)
            if isinstance(sv, GSBase):
                sub_gsbase = sv
                if isinstance(data_value, GStruct):
                    # Accept GStruct object that its GSBase is same with the one in definition
                    if data_value(sub_gsbase):
                        self.__dict__['__struct_data'][sk] = data_value
                    else:
                        raise ValueError("Unacceptable GStruct object of data key '{}'!".format(sk))
                elif isinstance(data_value, dict) or data_value is None:
                    # Convert dict object to GStruct object
                    self.__dict__['__struct_data'][sk] = sub_gsbase.new(data_value)
                else:
                    ValueError("Unexpected structure of data key '{}'!".format(sk))
            else:
                data_value = data_value if data_value is not None else sv
                if isinstance(data_value, GStruct):
                    data_value = data_value.data_
                self.__dict__['__struct_data'][sk] = data_value if data_value is not None else sv

    @property
    def gsbase_(self):
        return self.__dict__['__gsbase']

    @property
    def data_(self):
        data_obj = {}
        for sk, sv in self.__dict__['__struct_data'].items():
            if isinstance(sv, GStruct):
                data_obj[sk] = sv.data_
            else:
                data_obj[sk] = sv
        return data_obj

    def __iter__(self):
        return iter(self.data_.items())

    def __getattr__(self, item):
        """ Shortcut for get attribute value or method of this GStruct object """
        if item in self.__dict__['__struct_data']:
            return self.__dict__['__struct_data'][item]
        elif item in self.__dict__['__gsbase']:
            return self.__dict__['__gsbase'].make_method_call(item, self)
        else:
            raise AttributeError("Has no data key or method name '{}'!".format(item))

    def __setattr__(self, key, value):
        """ Shortcut for set attribute value of this GStruct object (NOT for GStruct method) """
        if key in self.__dict__['__struct_data']:
            self.__dict__['__struct_data'][key] = value
        else:
            raise KeyError("Data key not found!")

    def __len__(self):
        return len(self.__dict__['__struct_data'])

    def __contains__(self, item):
        return item in self.__dict__['__struct_data']

    def __copy__(self):
        """ Lead copy() to deepcopy() """
        return self.__deepcopy__()

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        new_data = {}
        for sk, sv in self.__dict__['__struct_data'].items():
            new_data[sk] = deepcopy(sv, memodict)
        new_obj = self.__class__(self.__dict__['__gsbase'], new_data)
        memodict[id(new_obj)] = new_obj
        return new_obj

    def __call__(self, *args, **kwargs):
        """ Shortcut for type inference of GStruct """
        dest_obj = args[0]
        flag = False
        if isinstance(dest_obj, GStruct):
            flag = self.gsbase_ == dest_obj.gsbase_
        elif isinstance(dest_obj, GSBase):
            gsbase = dest_obj
            flag = self.gsbase_ == gsbase
        elif isinstance(dest_obj, GSInterface):
            gsinterface = dest_obj
            flag = gsinterface.match(self.gsbase_)
        return flag
