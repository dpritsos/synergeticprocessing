
"""  """

#import multiprocessing.forking import _reduce_method, _reduce_method_descriptor 
import types
import sys
import os.path

def _reduce_method(m):
    print 'CALLING REDUCE FUNCTION'
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

#def _reduce_method(m):
#    print 'CALLING REDUCE FUNCTION'
    #__import__(m.im_func.__module__)
    #mod = sys.modules[m.im_func.__module__]
    #klass = getattr(mod, m.im_class.__name__)
#    if m.im_self is None:
#        pass # return getattr, (klass, m.im_func.__name__)
#    else:
#        print 'reduce getattr'
#        return _unpickle_method, (m.im_func.__name__, m.im_self, m.im_class)

def _unpickle_method(func_name, obj, cls):
    print 'CLASS NAME: ', cls
    cls.__module__ = cls.real_module
    method = getattr(obj, func_name)
    return method

def _reduce_method_descriptor(m):
    return getattr, (m.__objclass__, m.__name__)


def _pickle_method(method):
    print 'PICKLE'
    func_name = method.im_func.__name__
    obj = method.im_self #Use this only for Classes not including multiprocessing.Pool definition
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

registry = {}

class SynergeticMeta(type):
    def __new__(cls, name, bases, dict):
        __module__ = os.path.splitext(os.path.basename(__file__))[0]  ### look here ###
        print __module__
        #for attrib_name, attrib in dict.items():
        #    if isinstance(attrib, types.FunctionType):
        #        if not attrib_name.endswith('__'):
        #            registry[ attrib_name ] = True 
        return type.__new__(cls, name, bases, dict)
       
       
class Synergetic:
    __metaclass__ = SynergeticMeta

        
#Unit Test        
if __name__ == "__main__":
    
    import types
    import copy_reg
    copy_reg.pickle(types.MethodType, _reduce_method)
    copy_reg.pickle(types.MemberDescriptorType, _reduce_method_descriptor)
    #copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
    
    class Test(Synergetic): 
        
        def __init__(self):
            print 'INIT OK'
    
        def printme(self, li):
            print 'printing'       
            self.printone(li)
                
        def printone(self, i):
            print 'print one'
            print i
    
    from multiprocessing import Pool
    p = Pool(2)
    a = Test()
    lista  = [1, 2, 3, 4]
    p.imap(a.printone, lista, 4)
    p.close()
    p.join()
















