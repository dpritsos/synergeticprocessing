

from multiprocessing import Process, JoinableQueue

class aprocess(Process):
    
    def __init__(self, q):
        Process.__init__(self)
        self.feed = q
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            print 'Getting'
            print self.feed.get()
            self.feed.task_done()
            print 'Got it'
            

q = JoinableQueue()        
p = aprocess(q)
q.put('test')

q.join()

