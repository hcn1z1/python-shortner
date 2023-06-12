from threading import Thread


class Worker(Thread):  
    def run(self):
        self.value = None
        self.value = self._target(*self._args)