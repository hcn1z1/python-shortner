from threading import Thread


class Worker(Thread):  
    def run(self):
        self.value = None
        self.value = self._target(*self._args)

class ThreadReaper(Thread):
    def run(self):
        self.value = None
        while True : 
            try:self.value = self._target(*self._args)
            except:pass
            