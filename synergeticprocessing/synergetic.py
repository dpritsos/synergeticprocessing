
"""  """

#import multiprocessing.forking import _reduce_method, _reduce_method_descriptor 
import types
import sys
import os.path

def _reduce_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

def _reduce_method_descriptor(m):
    return getattr, (m.__objclass__, m.__name__)

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
    #def __reduce__(self):
    #    return getattr, (m.im_self, m.im_func.func_name)
        
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
















