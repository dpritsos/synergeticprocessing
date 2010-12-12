
from multiprocessing import Pool
import copy_reg
import types


#def _pickle_method(method):
    #if not registry[ method.im_func.__name__ ]:
    #    pass
#    print 'pass 1'
#    func_name = method.im_func.__name__
#    print 'pass 2'
#    obj = method.im_self #Use this only for Classes not including multiprocessing.Pool definition
#    print 'pass 3'
#    cls = method.im_class
#    print 'pass 4'
#    print ' PICKLING'
#    print 'pass 5'
#    return _unpickle_method, (func_name, obj, cls)

#def _unpickle_method(func_name, obj, cls):
#    print 'pass 6'
#    for cls in cls.__mro__:
#        try:
#            func = cls.__dict__[func_name]
#        except KeyError:
#            try:
#                pass #func = cls.__dict__[ '_' + cls.__name__ + func_name ]
#            except KeyError:
#                pass
#            else:
#                break
#        else:
#            break
    #print obj
#    return func.__get__(obj, cls)


def _pickle_method(method):
    func_name = method.im_func.__name__
    print func_name
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, cls)

def _unpickle_method(func_name, cls):
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(cls)


copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)



class test(object):
    def __init__(self):
        #self.p = Pool(2)
        #pass
        pass
        
    def feed(self):
        #self.test.im_func.__getstate__ = self.__getstate__
        #self.test.im_func.__setstate__ = self.__setstate__
        pass
        
    #def __getstate__(self):
    #    #for method in self.__dict__:
    #    print "test"
    #    obj = self
    #    cls = test
    #    return (obj, cls)
    
    #def __setstate__(self, func_name):
    #    for cls in cls.mro():
    #        try:
    #            func = cls.__dict__[func_name]
    #        except KeyError:
    #            pass
    #        else:
    #            break
    #    return func.__get__(cls)
    
    #def __get__(self, instance, cls):
    #    print 'USED'
    #    attrib = self.__dict__[name]
    #    if isinstance(attrib, types.MethodType):
    #        return getattr(self,attrib.im_func, attrib.im_class)
    
    #@staticmethod
    def test1(self, num):
        print num
            
    def pclose(self):
        #self.p.close()
        #self.p.join()
        pass

p = Pool(3)
c = test()
p.imap(c.test1, [1,2,3], 3)
p.close()
p.join()



