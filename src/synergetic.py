
"""  """

import types
import copy_reg

from multiprocessing import Pool

from pickle import Unpickler, Pickler

"""
class SynergeticMethod(object):
    
    def __init__(self, method):
        assert callable(method)
        self.method = method

    def __call__(self, obj, *args, **kwargs):
        return getattr(obj, self.method.__name__)(*args, **kwargs)

class SynergeticMeta(type):
    def __new__(cls, name, bases, dict):
        alter_dict = {}
        print name
        for attrib_name, attrib in dict.items():
            if isinstance(attrib, types.FunctionType):
                if not attrib_name.endswith('__'):
                    if attrib_name.startswith('__'):
                        new_fnc_name = attrib_name + '_origin'
                    else:
                        new_fnc_name = '__' + attrib_name + '_origin'
                    synmethod_name = attrib_name
                    alter_dict[ synmethod_name ] = SynergeticMethod(attrib)
                    alter_dict[ new_fnc_name ] = attrib
                else:
                    alter_dict[ attrib_name ] = attrib
            else:
                alter_dict[ attrib_name ] = attrib
            #change the instance dictionary with the new one
        dict = alter_dict
        print dict
        return type.__new__(cls, name, bases, dict)
        #self.__init__(self, name, bases, dict)                                         
"""         

def _pickle_method(method):
    if not registry[ method.im_func.__name__ ]:
        pass
    func_name = method.im_func.__name__
    obj = method.im_self #Use this only for Classes not including multiprocessing.Pool definition
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    print 'pass 6'
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            try:
                func = cls.__dict__[ '_' + cls.__name__ + func_name ]
            except KeyError:
                pass
            else:
                break
        else:
            break
    #print obj
    return func.__get__(obj, cls)


copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


registry = {}

class SynergeticMeta(type):
    def __new__(cls, name, bases, dict):
        for attrib_name, attrib in dict.items():
            if isinstance(attrib, types.FunctionType):
                if not attrib_name.endswith('__'):
                    registry[ attrib_name ] = True 
        return type.__new__(cls, name, bases, dict)
       
       
class Synergetic:
    __metaclass__ = SynergeticMeta


class Test(Synergetic): 
    
    def __init__(self):
        print 'INIT OK'
    
    def printme(self, li):
        print 'printing'       
        self.printone(li)
                
    def printone(self, i):
        print 'print one'
        print i

    
if __name__ == "__main__":
    p = Pool(2)
    a = Test()
    lista  = [1, 2, 3, 4]
    p.imap(a.printone, lista, 4)
    p.close()
    p.join()
















