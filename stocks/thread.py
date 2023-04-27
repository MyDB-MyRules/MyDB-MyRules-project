import threading
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render

options_to_execute = []

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
    def __init__(self, request, execution_time, transaction):
        self.transaction = transaction
        self.request = request
        self.execution_time = execution_time
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now notify the person")
            # notify
            options_to_execute.append(self.transaction)
            # messages.success(self.request, 'Your option %s has been executed. Please accept the transaction by proceeding to the accept_options page.' % self.transaction)
            
            # storage = messages.get_messages(self.request)
            # for message in storage:
            #     print(message)
            # storage.used = False
            
            redirect('dashboard')
                    
            print('abt to sleep again')
            # # sleep(float(self.execution_time)*2*60)
            sleep(120)
            options_to_execute.remove(self.transaction)
            print("timed out, removed from list")             
            
        except Exception as e:
            print(e)