
""" Worker Process: Implemented as part of the synergeticprocessing module
    Author: Dimitrios Pritsos
    Last update: 12 / Dec / 2010 """

from multiprocessing import Process 

class SynergeticProcess(Process):
    """SynergeticProcess class: Instantiation of this class is a process waiting infinitely for executing an incoming task. 
    'Worker' is properly defined for working in the Synergy Process Pool module called as synergeticprocessing.
    Arguments:
        tasks_queue: It should be a multiprocessing.JoinableQueue() or synergeticprocessing.JoinableQueue().
                     Contains a queue of tasks for the 'Worker' to execute. 
                     Each 'task' is a tuple (func, args).
                            task_id: Should be a unique integer. 
                                    Is used as reference ID for the Task was pushed to the task_queue
                                    and the results of Task execution pushed to the return_queue
                            Func: is the function for execution
                            args: *args tuple with data 
                            kwargs: **kwards dictionary with data 
        return_queue: It should be a multiprocessing.Queue() or synergeticprocessing.Queue().
                      Contains the results 'Func' returns. Each slot contains a tuple (task_id, Func_results)   
    Termination Signal:
        (None, None, None) : is the Sentinel signal for this process to terminate.
        More specifically when func == 'None' the process will terminate. 
        However, if Sentinel is not a tuple of 3 elements error will be raised.  
        That is, whenever a 'None' is received the process will close, and there is no
        way for the process to know if the None Signal has sent on purpose or because of a coding bug."""
       
    def __init__(self, tasks_queue, return_queue):
        Process.__init__(self)
        self.__tasks_q = tasks_queue
        self.__return_q = return_queue
        
    def run(self): 
        while True:
            print "Synergetic Process Works"
            #default value in case
            task_id, func, args, kwargs = self.__tasks_q.get()
            #assert func, "Error: <None> function was given for execution"
            if not func:
                return
            #if callable(func):
            #    raise Exception("synergeticprocessing.WorkerProcess error: Non-callable was given as function for execution")
            #Execute the function with its args
            func_ret = func( *args, **kwargs )
            #It should always be an available slot in the return queue or an exeption will me raised  
            self.__return_q.put_nowait( (task_id, func_ret) )
            self.__tasks_q.task_done()

