
""" Synergetic Server: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 13 / Dec / 2010 """
    
import types
import copy_reg
from multiprocessing import Process, Queue, JoinableQueue
from multiprocessing.connection import Listener
from synergeticprocess import SynergeticProcess
from synergetic import _reduce_method, _reduce_method_descriptor, _pickle_method, _unpickle_method

    
class SimpleSynergeticServer(Process):
    
    def __init__(self, authen_key):
        Process.__init__(self)
        self.__task_queue = JoinableQueue(1)
        self.__return_queue = Queue(1)
        self.serv = Listener(('', 40000), authkey=authen_key)
    
    def run(self):
        print 'Server Works'
        copy_reg.pickle(types.MethodType, _reduce_method, _unpickle_method)
        #Start the synergeticProcess in Deamon Mode
        worker_p = SynergeticProcess(self.__task_queue, self.__return_queue)
        worker_p.deamon = True
        worker_p.start()          
        while True:
            print 'wait for Client'
            pool_conn = self.serv.accept()
            print 'conneciton Client Accepted'
            while True:
                print 'in LOOP Simple sErver'
                #There is no need for task_id in this version
                try:
                    print 'Try to recv MSG'
                    unpickled_msg = pool_conn.recv()
                    print 'MSG REseved'
                except Exception as e: # EOFError:
                    print 'Fail To Receive MSG:', e
                    break 
                self.__task_queue.put(unpickled_msg)
                ret = self.__return_queue.get()
                try:
                    pool_conn.send( ret )
                except EOFError:
                    break
            pool_conn.close()    

if __name__ == '__main__':
    s = SimpleSynergeticServer('123456')
    s.start()
    
    while True:
        pass