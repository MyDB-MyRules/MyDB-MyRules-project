import threading
from time import sleep

class CreateThread1(threading.Thread):
    def __init__(self, func):
        self.function = func 
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            self.function()
        except Exception as e:
            print(e)  

class CreateThread2(threading.Thread):
    def __init__(self, execution_time):
        self.execution_time = execution_time
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now notify the person")
            # notify
        except Exception as e:
            print(e)