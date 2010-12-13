
""" Synergetic Process Pool: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 12 / Dec / 2010"""

import types
import copy_reg
#from threading import Thread, Event
from multiprocessing import Process, Queue, joinableQueue
from multiprocessing.connection import Client, Listener
from Queue import Empty
from synergetic import _reduce_method, _reduce_method_descriptor


class SynergeticPool(Process):
    """Synergetic Process Pool: """
    
    def __init__(self, synergetic_servers=None):
        #Enable Class Method Pickling  
        copy_reg.pickle(types.MethodType, _reduce_method)
        #Enable Descriptor Method Pickling
        copy_reg.pickle(types.MemberDescriptorType, _reduce_method_descriptor)
        #Keep the synergetic servers' IP Addresses or Names  
        self.__syn_servs = synergetic_servers
        #Synergetic Process available
        self.__syn_prcs = dict()
        #Start the Listener that is expecting new-coming synergetic-servers of synergetic-processes
        self.__start_synergetic_listener()
        #Start the Synergetic-Pool's functionality
        self.__start_pool 
        
    def __start_pool(self, local_worker_num=1):
        #Initialise the Queues
        syn_servs_num = len(self.__syn_servs)
        self.task_queue = JoinableQueue( syn_servs_num + local_worker_num )
        self.return_queue = Queue( syn_servs_num + local_worker_num )
        #Resize the Queues depending on Synergetic-Processes availability their state
        self.resize_pool(self, local_worker_num, self._syn_servs)
    
    def __start_synergetic_listener(self):
        listener = Process( target=self.__synergetic_serv_listener )
        listener.daemon = True
        listener.start()
    
    def __synegetic_serv_listener(self):
        serv = Listener(('', 41000), authkey='123456')
        while True:
            conn = serv.accept()
            try:
                server, port, authkey = conn.recv()
            except EOFError:
                recptn_failed = True
            if recptn_failed is False:
                conn.send('WELLCOME')
                conn.close()
                
       def resize_pool(self, local_worker_num=1, syn_servs):
           if len(self.__syn_prcs_avail) < local_worker_num:
              self.__syn_prcs_avail 
                
           
           for i in local_worker_num:
            
            
            
            
            
            
        
    
            
 
            
    def __remote_dispatch(self, ):

    def dispatch(self, *args):
        #This IF statement is only for self.map() function  
        if isinstance(args[0], tuple):
            args = args[0]
        #Check for proper number of arguments and fill the missing arguments 
        if len(args) == 3:
            self.__tasks_q.put( args )
        elif len(args) == 2:
            #If no callback-function is given return the result of the dispatched function to the dispatch caller
            #in that case this function waits until the results are available
            return_l = self.m.list()
            self.__tasks_q.put( (args[0], args[1], return_l.append) )
            while not return_l: #Maybe this should be become NON-BLOCKING
                pass
            return return_l[0]
        elif len(args) == 1:
            self.__tasks_q.put( (args[0], None, None) )
        else:
            raise Exception("ThreadPool spawn() Error: Bad number of argument has given")
    
    def map(self, func, callback=None, iterable=None):
        #Maps the self.dispatched function to all the date in a multi-threading manner 
        if callback:
            args_l = map( lambda i:(func, iterable[i], callback), range(len(iterable)) ) 
            for args in args_l:
                self.dispatch(args)
        else:
            args = map( lambda i:(func, iterable[i]), range(len(iterable)) ) 
            return map( lambda i: self.dispatch( args[i] ), range(len(args)) )
        #MAYBE an imap() (i.e. iterable object) function should be implemented too
    
    def join_all(self, timeout=None):
        """Clear the task queue and terminate all threads in Pool"""
        if timeout:
            self.__joinall.set()
            time_slice = float(timeout) / float( len(self.__threads_l) )
            for t in self.__threads_l:
                t.join(time_slice)
                del t
        else: 
            self.__tasks_q.join()
            self.__joinall.set() 
            for t in self.__threads_l:
                t.join()
                del t
    
    def count_threads(self):
        return len(self.__threads_l)


#Unit Test
if __name__ == "__main__":
    
    print "Unit test is running\n"
    
    # Simple task for testing
    def sorting(data):
        print("SortTask starting for: %s" % data)
        data.sort()
        print("SortTask done for: %s" % data)
        return "Data Sorted: ", data

    #Simple Callback_func for testing
    def callback_func(data):
        print("Callback Function => sorting() returned: %s \n" % str( data ) )

    #A pool or some worker threads 
    pool = ThreadPool(10)

    #Dispatch some tasks to the Thread Pool (i.e. put some entries at the task Queue of the ThreadPool instance)
    pool.dispatch(sorting, [5, 6, 7, 1, 3, 0, 1, 1, 10], callback_func)
    pool.dispatch(sorting, [5], callback_func)
    pool.dispatch(sorting, [0, 0, 1, 10], callback_func)
    #print("\npool.dispatch( sorting(), [ list ] ) returns: %s %s\n" % pool.dispatch(sorting, [5, 6, 7, 1, 3]) )   
    #print("pool.map() returns: %s \n\n" %  pool.map( sorting, iterable=([12, 1], [11, 1], [10, 1], [9, 1], [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1], [0, 1]) ) )
    #pool.map( sorting, callback=callback_func, iterable=([12, 1], [11, 1], [10, 1], [9, 1], [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1], [0, 1]) ) 
       
    #Terminate all threads when there are no other task for execution 
    pool.join_all()
    
    print("Thank you and Goodbye!")