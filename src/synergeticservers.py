
""" Synergetic Server: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 13 / Dec / 2010 """
    
from multiprocessing import Process, Queue
from multiprocessing.connection import Listener
from synergeticprocess import SynergeticProcess
    
class SimpleSynergeticServer(Process):
    
    def __init__(self, authen_key):
        Process.__init__(self)
        self.__task_queue = Queue(1)
        self.__return_queue = Queue(1)
        self.serv = Listener(('', 40000), authkey=authen_key)
    
    def run(self):
        print 'Server Works'
        #Start the synergeticProcess in Deamon Mode
        worker_p = SynergeticProcess(self.__task_queue, self.__return_queue)
        worker_p.deamon = True
        worker_p.start()          
        while True:
            pool_conn = self.serv.accept()
            while True:
                #There is no need for task_id in this version
                try:
                    unpickled_msg = pool_conn.recv()
                except EOFError:
                    break 
                self.task_queue.put(unpickled_msg)
                ret = self.return_queue.get()
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