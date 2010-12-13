
""" Synergetic Server: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 13 / Dec / 2010 """
    
from multiprocessing import Process, Queue
from multiprocessing.connection import Listener
from synergeticprocess import SynergeticProcess
    
class SimpleSynergeticServer(Process):
    
    def __init__(self, authen_key):
        self.task_queue = Queue(1)
        self.return_queue = Queue(1)
        self.serv = Listener(('', 40000), authkey=authen_key)
    
    def run(self):
        #Start the synergeticProcess in Deamon Mode
        worker_p = SynergeticProcess(task_queue= self.task_queue, return_queue=self.return_queue)
        worker_p.deamon = True
        worker_p.start()          
        while True:
            pool_conn = self.serv.accept()
            while True:
                #There is no need for task_id in this version
                task_id = None
                try:
                    func, args, kwargs = pool_conn.recv()
                except EOFError:
                    break
                unpickled_msg = (task_id, func, args, kwargs)
                self.task_queue.put(unpickled_msg)
                ret = self.return_queue.get()
                try:
                    pool_conn.send( ret )
                except EOFError:
                    break
            pool_conn.close()    
                
            
        