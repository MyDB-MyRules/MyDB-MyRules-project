import threading
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render
from .transactions import trade_contract

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
    def __init__(self, request, execution_time, transaction, buyer_name, seller_name):
        self.transaction = transaction
        self.request = request
        self.execution_time = execution_time
        self.buyer_name = buyer_name
        self.seller_name = seller_name
        threading.Thread.__init__(self)
    
    def run(self):
        from .views import send_message   
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now notify the person")
            # notify
            options_to_execute.append(self.transaction)
            send_message(self.seller_name, self.buyer_name, "Your option is mature. Process to accept or reject the transaction at Execute Mature Options page.")   
            print('abt to sleep again')
            sleep(120)
            options_to_execute.remove(self.transaction)
            print("timed out, removed from list")             
            
        except Exception as e:
            print(e)
            
class FuturesThread(threading.Thread):
    def __init__(self, request, execution_time, transaction, buyer_name, seller_name):
        self.transaction = transaction
        self.request = request
        self.execution_time = execution_time
        self.buyer_name = buyer_name
        self.seller_name = seller_name    
        threading.Thread.__init__(self)
    
    def run(self):
        from .views import send_message 
        try:
            print('abt to sleep')
            sleep(float(self.execution_time)*60)
            print("woke up, now execute the transaction")
            send_message(self.seller_name, self.buyer_name, "Your future has been executed") 
            txn = self.transaction
            # txn = [id, buyer_id, seller_id,stock_id,today,num_shares,price_per_share,5,premium,'options']
            # user_name = self.request.user.username
            # stock_id = self.transaction[3]
            # quantity = self.transaction[5]
            # buy_or_sell = True
            # price = self.transaction[6]
            # order = 'limit'  
                    
            trade_contract(txn[1],txn[2],txn[3],txn[4],txn[5],txn[6])                     
            
        except Exception as e:
            print(e)            