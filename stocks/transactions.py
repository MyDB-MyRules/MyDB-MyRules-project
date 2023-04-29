from datetime import date
from django.db import connection
import heapq
from collections import deque
import time
import enum

    
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

buy_orders  = {
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

sell_orders ={
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

market_buy  = {
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

market_sell  = {
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

stop_buy = {
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

stop_sell  = {
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

options_buy = {
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


futures_buy = {
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

# @transaction.atomic()
def trade_stock(user_name, stock_id, quantity , buy_or_sell,price , order):
    # Get the user and stock objects
    query = '''select id from customer where name = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query, [user_name])
        val = dictfetchall(cursor)
        user_id = val[0]['id']

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
    if user_port[0]['num_shares'] < quantity and buy_or_sell==False:
        raise ValueError("Not enough quantity of this stock to sell")
    
    if user[0]['balance'] < total_cost and buy_or_sell==True:
        raise ValueError("Not enough balance to buy this stock")

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
    # print(market_buy['ASIANPAINT'])
    # print(market_sell['ASIANPAINT'])
    # print(buy_orders['ASIANPAINT'])
    # print(sell_orders['ASIANPAINT'])
    
def trade_contract(buyer_id,seller_id,stock_id,date,num_shares,price_per_share):
    with connection.cursor() as cursor:
        cursor.execute(query1,[stock_id])
        stock = dictfetchall(cursor)

        
    query = '''SELECT max(id) FROM Transaction;'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        op = dictfetchall(cursor)
    buy_id = 1
    if(op[0]['max']!=None) :
        buy_id = int(op[0]['max']) + 1
        
    query = '''SELECT * from Customer where id=%s;'''
    with connection.cursor() as cursor:
        cursor.execute(query,[buyer_id])
        user = dictfetchall(cursor)
    new_value1 = user[0]['balance'] - price_per_share*num_shares
    # new_value2 = user.current_value + price_per_share*num_shares
    new_value2 = user[0]['invested_amount'] + price_per_share*num_shares
    query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
    with connection.cursor() as cursor:
        cursor.execute(query2,[new_value1,new_value2,buyer_id])
        connection.commit()
    #seller
    query = '''SELECT * from Customer where id=%s;'''
    with connection.cursor() as cursor:
        cursor.execute(query,[seller_id])
        user = dictfetchall(cursor)
    new_value1 = user[0]['balance'] + price_per_share*num_shares
    # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
    query2 = '''Update Customer SET balance = %s  WHERE id=%s;'''
    
    with connection.cursor() as cursor:
        cursor.execute(query2,[new_value1,seller_id])
        connection.commit()

    # INSERTING TRANSACTION
    
    sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
    val = [str(buy_id),buyer_id,seller_id , stock_id, date , num_shares , price_per_share]
    print(val)
    with connection.cursor() as cursor:
        cursor.execute(sql,val)
        connection.commit()
        
    # portfolio updation 
    #buyer
    query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
    with connection.cursor() as cursor:
        cursor.execute(query,[buyer_id,stock_id])
        user_port = dictfetchall(cursor)
    new_value1 = user_port[0]['invested_amount'] + price_per_share*num_shares
    new_value2 = user_port[0]['num_shares'] + num_shares
    query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query1,[new_value1, new_value2, buyer_id , stock_id])
        connection.commit()
    #seller
    query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
    with connection.cursor() as cursor:
        cursor.execute(query,[seller_id,stock_id])
        user_port = dictfetchall(cursor)
    # new_value1 = user_port[0]['invested_amount'] + price_per_share*num_shares
    new_value2 = user_port[0]['num_shares'] + num_shares
    query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query1,[new_value2, seller_id , stock_id])
        connection.commit()    
    
    #updated the stock_metadata price
    curr_price = price_per_share
    query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query,[stock_id])
        stock = dictfetchall(cursor)
    
    old_price = stock['price_per_share']
    final_price = (curr_price +old_price*1000.0)/1000.0
    query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query1,[final_price, stock_id])
        connection.commit()    

    #updated the portfolio price

    query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
    with connection.cursor() as cursor:
        cursor.execute(query,[stock_id])
        stock = dictfetchall(cursor)        

    for s in stock:
        query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
        with connection.cursor() as cursor:
            cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
            connection.commit()    

    query = '''select id from customer;'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        customers = dictfetchall(cursor)        

    for customer in customers:
        query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
        with connection.cursor() as cursor:
            cursor.execute(query1, [customer['id']])
            val = dictfetchall(cursor)
        query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
        with connection.cursor() as cursor:
            cursor.execute(query1, [val['sum'],customer['id']])
            connection.commit()

def transact():
    while(True):
        time.sleep(20)
        for key in buy_orders:
            # print(key)
            while transa(key) != -1 :
                print(888888888888)
            

#for a stock
# @transaction.atomic()
def transa(stock_id):

    today = date.today()
    today = date.isoformat(today)
    if len(stop_buy[stock_id])==0 and len(stop_sell[stock_id])==0 and len(market_buy[stock_id])==0 and len(market_sell[stock_id])==0 and (len(buy_orders[stock_id])==0 or len(sell_orders[stock_id])==0):
        # print(len(market_buy[stock_id]))
        return -1
    query = '''SELECT max(id) FROM Transaction;'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        op = dictfetchall(cursor)
    buy_id = 1
    if(op[0]['max']!=None) :
        # print(00000)
        buy_id = int(op[0]['max']) + 1
    # print(1)
    if(len(market_buy[stock_id])==0 and len(market_sell[stock_id])==0 and len(stop_buy[stock_id])==0 and len(stop_sell[stock_id])==0):
        buyt = heapq.heappop(buy_orders[stock_id])
        sellt= heapq.heappop(sell_orders[stock_id])
        
        if buyt[1].price_per_share>sellt[1].price_per_share:
            # print(33)
            if(buyt[1].num_shares>sellt[1].num_shares):
                buyt2 = buyt
                buyt2[1].num_shares = sellt[1].num_shares
                buyt2[1].price_per_share = sellt[1].price_per_share
                #buyer
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer])
                    user = dictfetchall(cursor)
                # print(109876)
                new_value1 = user[0]['balance'] - buyt2[1].price_per_share*buyt2[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                new_value2 = user[0]['invested_amount'] + buyt2[1].price_per_share*buyt2[1].num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt[1].customer])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + buyt2[1].price_per_share*buyt2[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                query2 = '''Update Customer SET balance = %s  WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,sellt[1].customer])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt[1].customer,sellt[1].customer , buyt[1].stock,today , sellt[1].num_shares , sellt[1].price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt[1].price_per_share*buyt2[1].num_shares
                new_value2 = user_port[0]['num_shares'] + buyt2[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt[1].customer , buyt[1].stock])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                # new_value1 = user_port[0]['invested_amount'] + sellt[1].price_per_share*buyt2[1].num_shares
                new_value2 = user_port[0]['num_shares'] + buyt2[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value2, sellt[1].customer , buyt[1].stock])
                    connection.commit()
                
                #updated the stock_metadata price
                curr_price = sellt[1].price_per_share
                query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)
                
                old_price = stock['price_per_share']
                final_price = (curr_price +old_price*1000.0)/1000.0
                query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price, stock_id])
                    connection.commit()    

                #updated the portfolio price

                query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)        

                for s in stock:
                    query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                        connection.commit()    

                query = '''select id from customer;'''
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    customers = dictfetchall(cursor)        

                for customer in customers:
                    query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [customer['id']])
                        val = dictfetchall(cursor)
                    query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [val['sum'],customer['id']])
                        connection.commit()


                #adding the remaining to queue
                buyt[1].num_shares -= sellt[1].num_shares
                heapq.heappush(buy_orders[stock_id], (-buyt[1].price_per_share, buyt))  
                
                
            elif buyt[1].num_shares<sellt[1].num_shares:
                sellt2 = sellt
                sellt2[1].num_shares = buyt[1].num_shares
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt2[1].price_per_share*sellt2[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                new_value2 = user[0]['invested_amount'] + sellt2[1].price_per_share*sellt2[1].num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt[1].customer])
                    connection.commit()
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + sellt2[1].price_per_share*sellt2[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                query2 = '''Update Customer SET balance = %s  WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,sellt[1].customer])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt[1].customer,sellt[1].customer , buyt[1].stock,today , buyt[1].num_shares , sellt[1].price_per_share]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt2[1].price_per_share*sellt2[1].num_shares
                new_value2 = user_port[0]['num_shares'] + sellt2[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt[1].customer , buyt[1].stock])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                # new_value1 = user_port[0]['invested_amount'] + sellt2[1].price_per_share*sellt2[1].num_shares
                new_value2 = user_port[0]['num_shares'] + sellt2[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value2, sellt[1].customer , buyt[1].stock])
                    connection.commit()


                curr_price = sellt2[1].price_per_share
                query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)
                
                old_price = stock['price_per_share']
                final_price = (curr_price +old_price*1000.0)/1000.0
                query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price, stock_id])
                    connection.commit()    

                #updated the portfolio price

                query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)        

                for s in stock:
                    query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                        connection.commit()    

                query = '''select id from customer;'''
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    customers = dictfetchall(cursor)        

                for customer in customers:
                    query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [customer['id']])
                        val = dictfetchall(cursor)
                    query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [val['sum'],customer['id']])
                        connection.commit()

                sellt[1].num_shares -= buyt[1].num_shares
                heapq.heappush(sell_orders[stock_id], (sellt[1].price_per_share, sellt))  
                
            else :
                # print(sellt[1].customer)
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - sellt[1].price_per_share*sellt[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                new_value2 = user[0]['invested_amount'] + sellt[1].price_per_share*sellt[1].num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt[1].customer])
                    connection.commit()
                # print(2)
                #seller
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer])
                    user = dictfetchall(cursor)
                # print(user)
                new_value1 = user[0]['balance'] + sellt[1].price_per_share*sellt[1].num_shares
                # new_value2 = user.current_value + buyt2[1].price_per_share*buyt[1].num_shares
                query2 = '''Update Customer SET balance = %s  WHERE id=%s;'''
                
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,sellt[1].customer])
                    connection.commit()
                # print(2)
                # INSERTING TRANSACTION
                
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [str(buy_id),buyt[1].customer,sellt[1].customer , buyt[1].stock, today , sellt[1].num_shares , sellt[1].price_per_share]
                print(val)
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                # print(3)
                # portfolio updation 
                #buyer
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + sellt[1].price_per_share*sellt[1].num_shares
                new_value2 = user_port[0]['num_shares'] + sellt[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt[1].customer , buyt[1].stock])
                    connection.commit()
                #seller
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                # new_value1 = user_port[0]['invested_amount'] + sellt[1].price_per_share*sellt[1].num_shares
                new_value2 = user_port[0]['num_shares'] + sellt[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value2, sellt[1].customer , buyt[1].stock])
                    connection.commit()

                curr_price = sellt[1].price_per_share
                query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)
                
                old_price = stock['price_per_share']
                final_price = (curr_price +old_price*1000.0)/1000.0
                query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price, stock_id])
                    connection.commit()    

                #updated the portfolio price

                query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)        

                for s in stock:
                    query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                        connection.commit()    

                query = '''select id from customer;'''
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    customers = dictfetchall(cursor)        

                for customer in customers:
                    query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [customer['id']])
                        val = dictfetchall(cursor)
                    query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [val['sum'],customer['id']])
                        connection.commit()

    elif len(stop_buy[stock_id])==0 and len(stop_sell[stock_id])==0:
        query1 = '''SELECT * from Stock_Metadata where symbol=%s;'''        
        with connection.cursor() as cursor:
            cursor.execute(query1,[stock_id])
            stock = dictfetchall(cursor)
            
        if len(market_buy[stock_id])!=0 :
            buyt = market_buy[stock_id].popleft()
            
            #UPDATING CUSTOMER
            query = '''SELECT * from Customer where id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[buyt.customer])
                user = dictfetchall(cursor)
            new_value1 = user[0]['balance'] - stock[0]['price_per_share']*buyt.num_shares
            new_value2 = user[0]['invested_amount'] + stock[0]['price_per_share']*buyt.num_shares
            query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query2,[new_value1,new_value2,buyt.customer])
                connection.commit()
                
            # INSERTING TRANSACTION
            sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
            val = [buy_id,buyt.customer,'0', buyt.stock,today , buyt.num_shares , stock[0]['price_per_share']]
            with connection.cursor() as cursor:
                cursor.execute(sql,val)
                connection.commit()
            
            # portfolio updation 
            query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[buyt.customer,buyt.stock])
                user_port = dictfetchall(cursor)
            new_value1 = user_port[0]['invested_amount'] + stock[0]['price_per_share']*buyt.num_shares
            new_value2 = user_port[0]['num_shares'] + buyt.num_shares
            query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query1,[new_value1, new_value2, buyt.customer , buyt.stock])
                connection.commit()

            curr_price = stock[0]['price_per_share']
            query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[stock_id])
                stock = dictfetchall(cursor)
            
            old_price = stock['price_per_share']
            final_price = (curr_price +old_price*1000.0)/1000.0
            query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query1,[final_price, stock_id])
                connection.commit()    

            #updated the portfolio price

            query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
            with connection.cursor() as cursor:
                cursor.execute(query,[stock_id])
                stock = dictfetchall(cursor)        

            for s in stock:
                query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                    connection.commit()    

            query = '''select id from customer;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                customers = dictfetchall(cursor)        

            for customer in customers:
                query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query1, [customer['id']])
                    val = dictfetchall(cursor)
                query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1, [val['sum'],customer['id']])
                    connection.commit()
      
        if len(market_sell[stock_id]) != 0 :
            sellt = market_sell[stock_id].popleft()
        
            query = '''SELECT * from Customer where id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[sellt.customer])
                user = dictfetchall(cursor)
            new_value1 = user[0]['balance'] + stock[0]['price_per_share']*sellt.num_shares
            query2 = '''Update Customer SET balance = %s WHERE id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query2,[new_value1,sellt.customer])
                connection.commit()
            
            
            # INSERTING TRANSACTION
            sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
            val = [buy_id,'0',sellt.customer , sellt.stock,today , sellt.num_shares , stock[0]['price_per_share']]
            with connection.cursor() as cursor:
                cursor.execute(sql,val)
                connection.commit()

            # portfolio UPDATION
            query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[sellt.customer,sellt.stock])
                user_port = dictfetchall(cursor)
            new_value2 = user_port[0]['num_shares'] + sellt.num_shares
            query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query1,[ new_value2, sellt.customer , sellt.stock])
                connection.commit()

            curr_price = stock[0]['price_per_share']
            query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query,[stock_id])
                stock = dictfetchall(cursor)
            
            old_price = stock['price_per_share']
            final_price = (curr_price +old_price*1000.0)/1000.0
            query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
            with connection.cursor() as cursor:
                cursor.execute(query1,[final_price, stock_id])
                connection.commit()    

            #updated the portfolio price

            query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
            with connection.cursor() as cursor:
                cursor.execute(query,[stock_id])
                stock = dictfetchall(cursor)        

            for s in stock:
                query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                    connection.commit()    

            query = '''select id from customer;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                customers = dictfetchall(cursor)        

            for customer in customers:
                query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query1, [customer['id']])
                    val = dictfetchall(cursor)
                query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1, [val['sum'],customer['id']])
                    connection.commit()

    
    else :
        query1 = '''SELECT * from Stock_Metadata where symbol=%s;'''        
        with connection.cursor() as cursor:
            cursor.execute(query1,[stock_id])
            stock = dictfetchall(cursor)
            
        if len(stop_buy[stock_id])!=0 :
            buyt = heapq.heappop(buy_orders[stock_id])
        
            if buyt[1].price_per_share >= stock[0]['price_per_share'] :
                #UPDATING CUSTOMER
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] - stock[0]['price_per_share']*buyt[1].num_shares
                new_value2 = user[0]['invested_amount'] + stock[0]['price_per_share']*buyt[1].num_shares
                query2 = '''Update Customer SET balance = %s , invested_amount = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,new_value2,buyt[1].customer])
                    connection.commit()
                    
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,buyt[1].customer,'0', buyt[1].stock,today , buyt[1].num_shares , stock[0]['price_per_share']]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()
                
                # portfolio updation 
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[buyt[1].customer,buyt[1].stock])
                    user_port = dictfetchall(cursor)
                new_value1 = user_port[0]['invested_amount'] + stock[0]['price_per_share']*buyt[1].num_shares
                new_value2 = user_port[0]['num_shares'] + buyt[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s, invested_amount = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[new_value1, new_value2, buyt[1].customer , buyt[1].stock])
                    connection.commit()

                curr_price = stock[0]['price_per_share']
                query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)
                
                old_price = stock['price_per_share']
                final_price = (curr_price +old_price*1000.0)/1000.0
                query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price, stock_id])
                    connection.commit()    

                #updated the portfolio price

                query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)        

                for s in stock:
                    query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                        connection.commit()    

                query = '''select id from customer;'''
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    customers = dictfetchall(cursor)        

                for customer in customers:
                    query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [customer['id']])
                        val = dictfetchall(cursor)
                    query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [val['sum'],customer['id']])
                        connection.commit()

        if len(stop_sell[stock_id]) != 0 :
            sellt= heapq.heappop(sell_orders[stock_id])
            if sellt[1].price_per_share <= stock[0]['price_per_share'] :
                query = '''SELECT * from Customer where id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer])
                    user = dictfetchall(cursor)
                new_value1 = user[0]['balance'] + stock[0]['price_per_share']*sellt[1].num_shares
                query2 = '''Update Customer SET balance = %s WHERE id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query2,[new_value1,sellt[1].customer])
                    connection.commit()
                
                
                # INSERTING TRANSACTION
                sql = '''INSERT INTO Transaction (id , buyer_id , seller_id ,stock_id , date , num_shares , price_per_share ) VALUES (%s, %s, %s , %s, %s, %s , %s);'''
                val = [buy_id,'0',sellt[1].customer , sellt[1].stock,today , sellt[1].num_shares , stock[0]['price_per_share']]
                with connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    connection.commit()

                # portfolio UPDATION
                query = '''SELECT * from Portfolio where customer_id=%s and stock_id=%s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[sellt[1].customer,sellt[1].stock])
                    user_port = dictfetchall(cursor)
                new_value2 = user_port[0]['num_shares'] + sellt[1].num_shares
                query1 = '''UPDATE Portfolio SET num_shares = %s WHERE customer_id = %s and stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[ new_value2, sellt[1].customer , sellt[1].stock])
                    connection.commit()

                curr_price = stock[0]['price_per_share']
                query = '''select price_per_share, symbol from stock_metadata where symbol = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)
                
                old_price = stock['price_per_share']
                final_price = (curr_price +old_price*1000.0)/1000.0
                query1 = '''UPDATE stock_metadata SET price_per_share = %s WHERE stock_id = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query1,[final_price, stock_id])
                    connection.commit()    

                #updated the portfolio price

                query = '''select customer_id, num_shares from portfolio where stock_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(query,[stock_id])
                    stock = dictfetchall(cursor)        

                for s in stock:
                    query1 = '''UPDATE portfolio SET current_value = %s WHERE customer_id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1,[final_price*s['num_shares'], s['customer_id']])
                        connection.commit()    

                query = '''select id from customer;'''
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    customers = dictfetchall(cursor)        

                for customer in customers:
                    query1 = '''select sum(current_value) from portfolio where customer_id = %s'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [customer['id']])
                        val = dictfetchall(cursor)
                    query1 = '''UPDATE customer SET current_value = %s WHERE id = %s;'''
                    with connection.cursor() as cursor:
                        cursor.execute(query1, [val['sum'],customer['id']])
                        connection.commit()

    return 0    
