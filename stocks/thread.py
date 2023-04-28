import threading
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render
from .transactions import trade_stock

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

class OptionsThread(threading.Thread):
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
                                
            print('abt to sleep again')
            sleep(120)
            options_to_execute.remove(self.transaction)
            print("timed out, removed from list")             
            
        except Exception as e:
            print(e)
            
class FuturesThread(threading.Thread):
    def __init__(self, request, execution_time, transaction):
        self.transaction = transaction
        self.request = request
        self.execution_time = execution_time
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now execute the transaction")
            
            # txn = [id, buyer_id, seller_id,stock_id,today,num_shares,price_per_share,5,premium,'options']
            user_name = self.request.user.username
            stock_id = self.transaction[3]
            quantity = self.transaction[5]
            buy_or_sell = True
            price = self.transaction[6]
            order = 'limit'  
                    
            trade_stock(user_name, stock_id, quantity , buy_or_sell,price, order)                        
            
        except Exception as e:
            print(e)            