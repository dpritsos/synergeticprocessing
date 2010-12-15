
""" Synergetic Process Pool: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 12 / Dec / 2010"""

import types
import copy_reg
#from threading import Thread, Event
from multiprocessing import Process, Queue, JoinableQueue
from multiprocessing.connection import Client, Listener
from Queue import Empty
from synergetic import Synergetic, _reduce_method, _reduce_method_descriptor, _pickle_method, _unpickle_method
from synergeticprocess import SynergeticProcess
from time import sleep
import random

class SynergeticPool(Process):
    """Synergetic Process Pool: """
    
    def __init__(self, synergetic_servers=None):
        #Enable Class Method Pickling
        #copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)  
        copy_reg.pickle(types.MethodType, _reduce_method)
        #Enable Descriptor Method Pickling
        copy_reg.pickle(types.MemberDescriptorType, _reduce_method_descriptor)
        #Dictionary of the synergetic servers' IP Addresses or Names with their connections  
        self.__syn_servs = dict()
        #List of available Synergetic Processes 
        self.__syn_pcss = list()
        #List of incomplete tasks recored
        self.__incomp_tasks = dict()
        #Start the Listener that is expecting new-coming synergetic-servers of synergetic-processes
        self.__start_synergetic_listener()
        #Start the Synergetic-Pool's functionality
        self.__start_pool(synergetic_servers, local_worker_num=1)
        #Start the Synergetic feeder that feeds the remote servers with Tasks  
        self.__start_synergetic_feeder()
        
    def __start_pool(self, synergetic_servers, local_worker_num=1):
        #Initialise the Queues
        if synergetic_servers:
            syn_servs_num = len(synergetic_servers)
        else:
            syn_servs_num = 0
        self.__task_queue = JoinableQueue( syn_servs_num + local_worker_num )
        self.__return_queue = Queue( syn_servs_num + local_worker_num )
        #
        #self.__start_local_pool(local_worker_num)
        #
        self.__start_serv_pool(synergetic_servers)
        
    def __start_synergetic_listener(self):
        listener = Process( target=self.__synergetic_serv_listener )
        listener.daemon = True
        listener.start()
    
    def __synergetic_serv_listener(self):
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
                
    def __start_synergetic_feeder(self):
        listener = Process( target=self.__synergetic_feeder )
        listener.daemon = True
        listener.start()  
    
    def __synergetic_feeder(self):
        while True:
            for serv_addr, conn in self.__syn_servs.items():
                #print 'Looking for Connection'
                if conn:
                    print 'connetion found'
                    Task = self.__task_queue.get()
                    self.__incomp_tasks[ Task[0] ] = Task
                    try:
                        conn.send( Task )
                        print 'TASK SENT'
                    except EOFError:
                        self.__syn_servs[ serv_addr ] = None
            for serv_addr, conn in self.__syn_servs.items():
                if conn:
                    try:
                        return_msg = conn.recv()
                    except EOFError:
                        self.__syn_servs[ serv_addr ] = None
                    else:
                        del self.__incomp_tasks[ return_msg[0] ]
                        self.__return_queue.put( return_msg )
            for incomp_task in self.__incomp_tasks.values():
                self.__task_queue.put( incomp_task )
    
    def __synergetic_serv_connection(self, serv, port, auth):
        try:
            print 'Conneting'
            print serv, port, auth
            conn = Client((str(serv), port), authkey=str(auth))
            print 'Conneted'
        except:
            conn = None
        return conn
    
    def __start_local_pool(self, local_worker_num=1):
        for i in range(local_worker_num):
            self.__syn_pcss.append( SynergeticProcess(self.__task_queue, self.__return_queue) )
        for syn_p in self.__syn_pcss:
            syn_p.daemonic = True
            syn_p.start()
                
    def __start_serv_pool(self, synergetic_servers):
        for serv, (port, auth) in synergetic_servers.items():
            print serv, port, auth
            conn = self.__synergetic_serv_connection(serv, port, auth)
            if conn:
                print 'POOL OPEND'
                self.__syn_servs[ serv ] = conn
            else:
                #Maybe this will be DEPRICATED 
                self.__syn_servs[ serv ] = None    

    def __dispatch(self, func, *args, **kwargs):
        task_id = str( random.randrange(1, 100000000) )
        task = (task_id, func, args, kwargs)
        self.__task_queue.put( task )
        return task_id
    
    def dispatch(self, func, *args, **kwargs):
        task_id = self.__dispatch(func, *args, **kwargs)
        return ResaultIterator(self.__return_queue, [task_id])
    
    def imap(self, func, iterable=None, chank=1, callback=None):
        task_ids = list()
        if chank == 1:
            for itr_item in iterable:
                task_id = self.__dispatch( func, itr_item )
                task_ids.append( task_id )
        else:
            chank_size = len(iterable) / chank
            chank_res_num = len(iterable) % chank
            for i in range(chank):
                start_pntr = i * chank_size
                end_pntr = (i+1) * chank_size
                itr_chank = iterable[ start_pntr:end_pntr ]
                task_id = self.__dispatch( func, itr_chank )
                task_ids.append( task_id ) 
            if chank_res_num:
                itr_chank = iterable[ end_pntr:(end_pntr + chank_res_num) ]
                task_id = self.__dispatch( func, itr_chank )
                task_ids.append( task_id )
        return ResaultIterator( self.__return_queue, task_ids )    
    
    def map(self, func, iterable=None, chank=1, callback=None):
        ret = list()
        iter_ret = self.imap(func, iterable, chank, callback)
        for ret_item in iter_ret:
            ret.append( ret_item )
    
    def join_all(self, timeout=None):
        pass
    
    @property
    def remote_prcss_num(self):
        return len(self.__syn_pcss)
    
    @property
    def local_prcss_num(self):
        return len(self.__syn_servs)
    

class ResaultIterator(object):
    
    def __init__(self, return_queue, tasks):
        self.__return_queue = return_queue
        self.__tasks = tasks
    
    def __iter__(self):
        return self
    
    def next(self):
        ret = self.value
        if ret == 'None':
            raise StopIteration
        return ret
    
    @property
    def value(self):
        ret = 'None'
        while self.__tasks:
            print 'Blocks'
            ret = self.__return_queue.get()
            print 'Blocks', ret
            task_id = ret[0]
            if task_id in self.__tasks:
                self.__tasks.remove( task_id )
                break
            else:
                self.__return_queue.put()
        return ret

import os.path

class sor(object):
    real_module = os.path.splitext(os.path.basename(__file__))[0]
    #__module__ = os.path.splitext(os.path.basename(__file__))[0]  ### look here ###
    def sorting(self, data):
        print("SortTask starting for: %s" % data)
        data.sort()
        print("SortTask done for: %s" % data)
        return "Data Sorted: ", data

#Unit Test
if __name__ == "__main__":
    
    print "Unit test is running\n"
    #import sys
    #mod = __import__(__name__)
    #import testclass 
    #mod = sys.modules[__name__]
    from testclass import sor
    srt = sor()

    #Simple Callback_func for testing
    def callback_func(data):
        print("Callback Function => sorting() returned: %s \n" % str( data ) )

    #A pool or some worker threads 
    pool = SynergeticPool( { '192.168.1.65':(40000,'123456') } )

    #Dispatch some tasks to the Thread Pool (i.e. put some entries at the task Queue of the ThreadPool instance)
    for ret in pool.dispatch(srt.sorting, [5, 6, 7, 1, 3, 0, 1, 1, 10]):
        print 'RET', ret
    #pool.dispatch(sorting, [5], callback_func)
    #pool.dispatch(sorting, [0, 0, 1, 10], callback_func)
    #print("\npool.dispatch( sorting(), [ list ] ) returns: %s %s\n" % pool.dispatch(sorting, [5, 6, 7, 1, 3]) )   
    #print("pool.map() returns: %s \n\n" %  pool.map( sorting, iterable=([12, 1], [11, 1], [10, 1], [9, 1], [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1], [0, 1]) ) )
    #pool.map( sorting, callback=callback_func, iterable=([12, 1], [11, 1], [10, 1], [9, 1], [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1], [0, 1]) ) 
       
    #Terminate all threads when there are no other task for execution 
    pool.join_all()
    
    print("Thank you and Goodbye!")
    
    
    