from django.db import transaction
from .models import Transaction, Portfolio , Customer , StockMetadata
from datetime import date
from django.db import connection
import heapq
from collections import deque



class transactn:
    def __init__(self, customer , stock , date , num_shares , price_per_share ):
        self.customer = customer
        self.stock = stock 
        self.date = date
        self.num_shares= num_shares
        self.price_per_share = price_per_share
    
def dictfetchall(cursor):
    desc = cursor.description     
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

buy_orders = stock_dict = {
    'ADANIPORTS': [],
    'ASIANPAINT': [],
    'AXISBANK': [],
    'BAJAJAUTO': [],
    'BAJAJFINSV': [],
    'BAJFINANCE': [],
    'BHARTIARTL': [],
    'BPCL': [],
    'BRITANNIA': [],
    'CIPLA': [],
    'COALINDIA': [],
    'DRREDDY': [],
    'EICHERMOT': [],
    'GAIL': [],
    'GRASIM': [],
    'HCLTECH': [],
    'HDFC': [],
    'HDFCBANK': [],
    'HEROMOTOCO': [],
    'HINDALCO': [],
    'HINDUNILVR': [],
    'ICICIBANK': [],
    'INDUSINDBK': [],
    'INFRATEL': [],
    'INFY': [],
    'IOC': [],
    'ITC': [],
    'JSWSTEEL': [],
    'KOTAKBANK': [],
    'LT': [],
    'M&M': [],
    'MARUTI': [],
    'NESTLEIND': [],
    'NTPC': [],
    'ONGC': [],
    'POWERGRID': [],
    'RELIANCE': [],
    'SBIN': [],
    'SHREECEM': [],
    'SUNPHARMA': [],
    'TATAMOTORS': [],
    'TATASTEEL': [],
    'TCS': [],
    'TECHM': [],
    'TITAN': [],
    'ULTRACEMCO': [],
    'UPL': [],
    'VEDL': [],
    'WIPRO': [],
    'ZEEL': []
}

sell_orders = stock_dict = {
    'ADANIPORTS': [],
    'ASIANPAINT': [],
    'AXISBANK': [],
    'BAJAJAUTO': [],
    'BAJAJFINSV': [],
    'BAJFINANCE': [],
    'BHARTIARTL': [],
    'BPCL': [],
    'BRITANNIA': [],
    'CIPLA': [],
    'COALINDIA': [],
    'DRREDDY': [],
    'EICHERMOT': [],
    'GAIL': [],
    'GRASIM': [],
    'HCLTECH': [],
    'HDFC': [],
    'HDFCBANK': [],
    'HEROMOTOCO': [],
    'HINDALCO': [],
    'HINDUNILVR': [],
    'ICICIBANK': [],
    'INDUSINDBK': [],
    'INFRATEL': [],
    'INFY': [],
    'IOC': [],
    'ITC': [],
    'JSWSTEEL': [],
    'KOTAKBANK': [],
    'LT': [],
    'M&M': [],
    'MARUTI': [],
    'NESTLEIND': [],
    'NTPC': [],
    'ONGC': [],
    'POWERGRID': [],
    'RELIANCE': [],
    'SBIN': [],
    'SHREECEM': [],
    'SUNPHARMA': [],
    'TATAMOTORS': [],
    'TATASTEEL': [],
    'TCS': [],
    'TECHM': [],
    'TITAN': [],
    'ULTRACEMCO': [],
    'UPL': [],
    'VEDL': [],
    'WIPRO': [],
    'ZEEL': []
}

market_buy = stock_dict = {
    'ADANIPORTS': deque(),
    'ASIANPAINT': deque(),
    'AXISBANK': deque(),
    'BAJAJAUTO': deque(),
    'BAJAJFINSV': deque(),
    'BAJFINANCE': deque(),
    'BHARTIARTL': deque(),
    'BPCL': deque(),
    'BRITANNIA': deque(),
    'CIPLA': deque(),
    'COALINDIA': deque(),
    'DRREDDY': deque(),
    'EICHERMOT': deque(),
    'GAIL': deque(),
    'GRASIM': deque(),
    'HCLTECH': deque(),
    'HDFC': deque(),
    'HDFCBANK': deque(),
    'HEROMOTOCO': deque(),
    'HINDALCO': deque(),
    'HINDUNILVR': deque(),
    'ICICIBANK': deque(),
    'INDUSINDBK': deque(),
    'INFRATEL': deque(),
    'INFY': deque(),
    'IOC': deque(),
    'ITC': deque(),
    'JSWSTEEL': deque(),
    'KOTAKBANK': deque(),
    'LT': deque(),
    'M&M': deque(),
    'MARUTI': deque(),
    'NESTLEIND': deque(),
    'NTPC': deque(),
    'ONGC': deque(),
    'POWERGRID': deque(),
    'RELIANCE': deque(),
    'SBIN': deque(),
    'SHREECEM': deque(),
    'SUNPHARMA': deque(),
    'TATAMOTORS': deque(),
    'TATASTEEL': deque(),
    'TCS': deque(),
    'TECHM': deque(),
    'TITAN': deque(),
    'ULTRACEMCO': deque(),
    'UPL': deque(),
    'VEDL': deque(),
    'WIPRO': deque(),
    'ZEEL': deque()
}

market_sell = stock_dict = {
    'ADANIPORTS': deque(),
    'ASIANPAINT': deque(),
    'AXISBANK': deque(),
    'BAJAJAUTO': deque(),
    'BAJAJFINSV': deque(),
    'BAJFINANCE': deque(),
    'BHARTIARTL': deque(),
    'BPCL': deque(),
    'BRITANNIA': deque(),
    'CIPLA': deque(),
    'COALINDIA': deque(),
    'DRREDDY': deque(),
    'EICHERMOT': deque(),
    'GAIL': deque(),
    'GRASIM': deque(),
    'HCLTECH': deque(),
    'HDFC': deque(),
    'HDFCBANK': deque(),
    'HEROMOTOCO': deque(),
    'HINDALCO': deque(),
    'HINDUNILVR': deque(),
    'ICICIBANK': deque(),
    'INDUSINDBK': deque(),
    'INFRATEL': deque(),
    'INFY': deque(),
    'IOC': deque(),
    'ITC': deque(),
    'JSWSTEEL': deque(),
    'KOTAKBANK': deque(),
    'LT': deque(),
    'M&M': deque(),
    'MARUTI': deque(),
    'NESTLEIND': deque(),
    'NTPC': deque(),
    'ONGC': deque(),
    'POWERGRID': deque(),
    'RELIANCE': deque(),
    'SBIN': deque(),
    'SHREECEM': deque(),
    'SUNPHARMA': deque(),
    'TATAMOTORS': deque(),
    'TATASTEEL': deque(),
    'TCS': deque(),
    'TECHM': deque(),
    'TITAN': deque(),
    'ULTRACEMCO': deque(),
    'UPL': deque(),
    'VEDL': deque(),
    'WIPRO': deque(),
    'ZEEL': deque()
}

stop_buy= stock_dict = {
    'ADANIPORTS': [],
    'ASIANPAINT': [],
    'AXISBANK': [],
    'BAJAJAUTO': [],
    'BAJAJFINSV': [],
    'BAJFINANCE': [],
    'BHARTIARTL': [],
    'BPCL': [],
    'BRITANNIA': [],
    'CIPLA': [],
    'COALINDIA': [],
    'DRREDDY': [],
    'EICHERMOT': [],
    'GAIL': [],
    'GRASIM': [],
    'HCLTECH': [],
    'HDFC': [],
    'HDFCBANK': [],
    'HEROMOTOCO': [],
    'HINDALCO': [],
    'HINDUNILVR': [],
    'ICICIBANK': [],
    'INDUSINDBK': [],
    'INFRATEL': [],
    'INFY': [],
    'IOC': [],
    'ITC': [],
    'JSWSTEEL': [],
    'KOTAKBANK': [],
    'LT': [],
    'M&M': [],
    'MARUTI': [],
    'NESTLEIND': [],
    'NTPC': [],
    'ONGC': [],
    'POWERGRID': [],
    'RELIANCE': [],
    'SBIN': [],
    'SHREECEM': [],
    'SUNPHARMA': [],
    'TATAMOTORS': [],
    'TATASTEEL': [],
    'TCS': [],
    'TECHM': [],
    'TITAN': [],
    'ULTRACEMCO': [],
    'UPL': [],
    'VEDL': [],
    'WIPRO': [],
    'ZEEL': []
}

stop_sell = stock_dict = {
    'ADANIPORTS': [],
    'ASIANPAINT': [],
    'AXISBANK': [],
    'BAJAJAUTO': [],
    'BAJAJFINSV': [],
    'BAJFINANCE': [],
    'BHARTIARTL': [],
    'BPCL': [],
    'BRITANNIA': [],
    'CIPLA': [],
    'COALINDIA': [],
    'DRREDDY': [],
    'EICHERMOT': [],
    'GAIL': [],
    'GRASIM': [],
    'HCLTECH': [],
    'HDFC': [],
    'HDFCBANK': [],
    'HEROMOTOCO': [],
    'HINDALCO': [],
    'HINDUNILVR': [],
    'ICICIBANK': [],
    'INDUSINDBK': [],
    'INFRATEL': [],
    'INFY': [],
    'IOC': [],
    'ITC': [],
    'JSWSTEEL': [],
    'KOTAKBANK': [],
    'LT': [],
    'M&M': [],
    'MARUTI': [],
    'NESTLEIND': [],
    'NTPC': [],
    'ONGC': [],
    'POWERGRID': [],
    'RELIANCE': [],
    'SBIN': [],
    'SHREECEM': [],
    'SUNPHARMA': [],
    'TATAMOTORS': [],
    'TATASTEEL': [],
    'TCS': [],
    'TECHM': [],
    'TITAN': [],
    'ULTRACEMCO': [],
    'UPL': [],
    'VEDL': [],
    'WIPRO': [],
    'ZEEL': []
}

#adding and subracting in portdolio

@transaction.atomic()
def trade_stock(user_id, stock_id, quantity , buy_or_sell,price , order):
    # Get the user and stock objects
    query = '''SELECT * from Customer where id=%s;'''
    query1 = '''SELECT * from Stock_Metadata where symbol=%s;'''
    query2 = '''SELECT * from Portfolio where  customer_id=%s and stock_id=%s;'''
    
    with connection.cursor() as cursor:
        cursor.execute(query,[user_id])
        user = dictfetchall(cursor)
        
    with connection.cursor() as cursor:
        cursor.execute(query1,[stock_id])
        stock = dictfetchall(cursor)
        
    with connection.cursor() as cursor:
        cursor.execute(query2,[user_id,stock_id])
        user_port = dictfetchall(cursor)
        
    
    
    # user = Customer.objects.get(id=user_id)
    # stock = StockMetadata.objects.get(symbol=stock_id)
    # user_port = Portfolio.objects.get(customer=user_id,stock=stock_id)
    
    today = date.today()
    
    # total_cost = quantity * stock[0]['price_per_share']
    
    # # No. of shares are initialised to 0 when a profile is created for a customer
    # # Check if the user has enough quantity of the stock to sell
    # if user_port[0]['num_shares'] < quantity and buy_or_sell==False:
    #     raise ValueError("Not enough quantity of this stock to sell")
    
    # if user[0]['balance'] < total_cost and buy_or_sell==True:
    #     raise ValueError("Not enough balance to buy this stock")

    # Calculate the total revenue of the transaction
    # total_revenue = quantity * stock.price_per_share
    if(order == 'limit') :
        # Create a new transactn object
        trans = transactn(
            customer=user_id,
            stock=stock_id,
            date = today,
            num_shares=quantity,
            price_per_share =price
        )
        if buy_or_sell == False:
            heapq.heappush(sell_orders[stock_id], (price, trans))
        else:
            heapq.heappush(buy_orders[stock_id], (-price, trans))
    elif order == 'market' :
        if(buy_or_sell==True):
            trans = transactn(
                customer=user_id,
                stock=stock_id,
                date = today,
                num_shares=quantity,
                price_per_share = stock[0]['price_per_share']
            )
            market_buy[stock_id].append(trans)
        else:
            trans = transactn(
                customer=user_id,
                stock=stock_id,
                date = today,
                num_shares=quantity,
                price_per_share = stock[0]['price_per_share']
            )
            market_sell[stock_id].append(trans)       
    else :
        if(buy_or_sell==True):
            trans = transactn(
                customer=user_id,
                stock=stock_id,
                date = today,
                num_shares=quantity,
                price_per_share = price
            )
            heapq.heappush(stop_buy[stock_id], (-price, trans))
        else:
            trans = transactn(
                customer=user_id,
                stock=stock_id,
                date = today,
                num_shares=quantity,
                price_per_share = price
            )
            heapq.heappush(stop_sell[stock_id], (price, trans)) 
        
    # print(buy_orders)
    # print(sell_orders)
    print(market_buy)
@transaction.atomic()
def transact():
    for key in buy_orders:
        while transa(key) != -1 :
            continue

#for a stock
@transaction.atomic()
def transa(stock_id):
    if(len(market_buy[stock_id])==0 and len(buy_orders[stock_id])==0) or (len(market_sell[stock_id])==0 and len(sell_orders[stock_id])==0):
        return -1
        
    query = '''SELECT max(id) FROM Transaction;'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        op = dictfetchall(cursor)
    buy_id = int(op[0]['max']) + 1
    if(len(market_buy[stock_id])==0 and len(market_sell[stock_id])==0):
        buyt = heapq.heappop(buy_orders[stock_id])
        sellt= heapq.heappop(sell_orders[stock_id])
        
        if buyt.price_per_share>=sellt.price_per_share:
            if(buyt.num_shares>sellt.num_shares):
                buyt2 = buyt
                buyt2.num_shares = sellt.num_shares
                buyt2.price_per_share = sellt.price_per_share
                #buyer
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - buyt2.price_per_share*buyt2.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + buyt2.price_per_share*buyt2.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + buyt2.price_per_share*buyt2.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt2.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt2.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt2.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt2.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                
                #adding the remaining to queue
                buyt.num_shares -= sellt.num_shares
                heapq.heappush(buy_orders[stock_id], (-buyt.price_per_share, buyt))  
                
                
            elif buyt.num_shares<sellt.num_shares:
                sellt2 = sellt
                sellt2.num_shares = buyt.num_shares
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt2.price_per_share*sellt2.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt2.price_per_share*sellt2.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt2.price_per_share*sellt2.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , buyt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt2.price_per_share*sellt2.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt2.price_per_share*sellt2.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt2.price_per_share*sellt2.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt2.price_per_share*sellt2.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                sellt.num_shares -= buyt.num_shares
                heapq.heappush(sell_orders[stock_id], (sellt.price_per_share, sellt))  
                
            else :
                
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                
    else:
        if(len(market_buy[stock_id])==0):
            sellt = market_sell[stock_id].popleft(0)
            buyt = heapq.heappop(buy_orders[stock_id])
            if(buyt.num_shares>sellt.num_shares):
                #buyer
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - buyt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + buyt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + buyt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , buyt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + buyt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + buyt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + buyt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + buyt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                
                #adding the remaining to queue
                buyt.num_shares -= sellt.num_shares
                heapq.heappush(buy_orders[stock_id], (-buyt.price_per_share, buyt))  
                
            elif buyt.num_shares<sellt.num_shares:
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - buyt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + buyt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , buyt.num_shares , buyt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + buyt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + buyt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + buyt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + buyt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                sellt.num_shares -= buyt.num_shares
                market_sell[stock_id].appendleft(sellt)  
                
            else :
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
            
        elif(len(market_sell[stock_id])==0):
            buyt = market_buy[stock_id].popleft(0)
            sellt= heapq.heappop(sell_orders[stock_id])
            if(buyt.num_shares>sellt.num_shares):
                #buyer
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                
                #adding the remaining to queue
                buyt.num_shares -= sellt.num_shares
                market_buy[stock_id].appendleft(buyt)  
                
                
            elif buyt.num_shares<sellt.num_shares:
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , buyt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                sellt.num_shares -= buyt.num_shares
                heapq.heappush(sell_orders[stock_id], (sellt.price_per_share, sellt))  
                
            else :
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
        
        else:
            buyt = market_buy[stock_id].popleft(0)
            sellt = market_sell[stock_id].popleft(0)
            if(buyt.num_shares>sellt.num_shares):
                #buyer
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                
                #adding the remaining to queue
                buyt.num_shares -= sellt.num_shares
                market_buy[stock_id].appendleft(buyt)  
                
                
            elif buyt.num_shares<sellt.num_shares:
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*buyt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , buyt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*buyt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*buyt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
                sellt.num_shares -= buyt.num_shares
                market_sell[stock_id].appendleft(sellt)  
                
            else :
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                new_value2 = user[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt.customer_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.customer_id])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt.price_per_share*sellt.num_shares
                # new_value2 = user.current_value + buyt.price_per_share*buyt.num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,sellt.customer_id])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt.customer_id,sellt.customer_id , buyt.stock_id,date , sellt.num_shares , sellt.price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt.user_id , buyt.stock_id])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt.user_id,buyt.stock_id])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt.price_per_share*sellt.num_shares
                new_value2 = user_port[0]['num_shares'] + sellt.price_per_share*sellt.num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, sellt.user_id , buyt.stock_id])
                    connection.commit()
    return 0    