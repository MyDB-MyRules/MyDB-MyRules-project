import threading
from time import sleep
from django.contrib import messages

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
    def __init__(self, request, derivative_id, execution_time):
        self.derivative_id = derivative_id
        self.request = request
        self.execution_time = execution_time
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now notify the person")
            # notify
            messages.success(self.request, 'Your option %s has been executed. Please accept the transaction by proceeding to the accept_options page.' % self.derivative_id)
            print('Your option %s has been executed. Please accept the transaction by proceeding to the accept_options page.' % self.derivative_id)
            
        except Exception as e:
            print(e)