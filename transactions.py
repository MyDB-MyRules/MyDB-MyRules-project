from django.db import transaction
from .models import Transaction, Portfolio , Customer , StockMetadata
from datetime import date
from django.db import connection
import heapq

def dictfetchall(cursor):
    desc = cursor.description     
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

buy_orders = []
sell_orders = []

#adding and subracting in portdolio

@transaction.atomic()
def trade_stock(user_id, stock_id, quantity , buy_or_sell,price ,order):
    # Get the user and stock objects
    query = '''SELECT * from Customer where id=user_id;'''
    query1 = '''SELECT * from StockMetadata where symbol=stock_id;'''
    query2 = '''SELECT * from Portfolio where customer=user_id and stock=stock_id;'''
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        user = dictfetchall(cursor)
        
    with connection.cursor() as cursor:
        cursor.execute(query1)
        stock = dictfetchall(cursor)
        
    with connection.cursor() as cursor:
        cursor.execute(query2)
        user_port = dictfetchall(cursor)
        
    
    
    # user = Customer.objects.get(id=user_id)
    # stock = StockMetadata.objects.get(symbol=stock_id)
    # user_port = Portfolio.objects.get(customer=user_id,stock=stock_id)
    
    today = date.today()
    
    total_cost = quantity * stock.price_per_share
    
    # No. of shares are initialised to 0 when a profile is created for a customer
    # Check if the user has enough quantity of the stock to sell
    if user_port.num_shares < quantity and buy_or_sell==False:
        raise ValueError("Not enough quantity of this stock to sell")
    
    if user.balance < total_cost and buy_or_sell==True:
        raise ValueError("Not enough balance to buy this stock")

    # Calculate the total revenue of the transaction
    # total_revenue = quantity * stock.price_per_share

    # Create a new transaction object
    transaction = Transaction(
        id=1,
        customer=user_id,
        stock=stock_id,
        date = today,
        num_shares=quantity,
        price_per_share =price,
        buy_or_sell=buy_or_sell
    )

    # Update the user balance and stock quantity
    # user.balance += total_revenue
    if buy_or_sell == False:
        heapq.heappush(sell_orders, (price, transaction))
    else:
        heapq.heappush(buy_orders, (-price, transaction))
    
    # Save the changes to the database
    # user.save()
    # stock.save()
    # transaction.save()


def transact():
    buyt = heapq.nsmallest(1,buy_orders)[1]
    sellt = heapq.nsmallest(1,sell_orders)[1]
    if buyt.price_per_share>=sellt.price_per_share :
        if(buyt.num_shares>sellt.num_shares):
            buyt2 = buyt
            buyt2.num_shares = sellt.num_shares
            buyt2.price_per_share = sellt.price_per_share
            query = '''SELECT max(id) FROM Transaction;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                op = dictfetchall(cursor)
            # print(op)
            buy_id = int(op[0]['max']) + 1
            sell_id = int(op[0]['max']) + 2
            query = '''SELECT * from Customer where id=user_id;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = dictfetchall(cursor)
            new_value1 = user.balance - buyt2.price_per_share*buyt.num_shares
            new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
            new_value3 = user.invested_amount + buyt2.price_per_share*buyt.num_shares
            query2 = '''Update Customer SET balance = %s , current_value = %s , invested_amount = %s , (new_value1,new_value2,new_value3);'''
            with connection.cursor() as cursor:
                cursor.execute(query2)
                connection.commit()
            sql = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s);"
            sql2 = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s);"
            with connection.cursor() as cursor:
                cursor.execute(sql,val)
                connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(sql2,val1)
                connection.commit()

            # buyt2.save()
            # sellt2.save()
            buyt.num_shares -= sellt.num_shares
            heapq.heapreplace(buy_orders, (-buyt.price_per_share, transaction))  
            # user_port = Portfolio.objects.get(customer=buyt.user_id,stock=buyt.stock_id)
            # portfolio updation 
            query = '''SELECT * from Portfolio where customer=buyt.user_id and stock=buyt.stock_id;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user_port = dictfetchall(cursor)
            query1 = '''UPDATE Portfolio SET num_shares = %s, investes_amount = %s , current_value = %s WHERE customer = %s and stock = %s", (new_value1, new_value2,new_value3 , buyt.user_id , buyt.stock_id);'''
            with connection.cursor() as cursor:
                cursor.execute(query1)
                connection.commit()
            
        elif buyt.num_shares<sellt.num_shares:
            sellt2 = sellt
            sellt2.num_shares = buyt.num_shares
            sellt2.price_per_share = buyt.price_per_share
            query = '''SELECT max(id) FROM Transaction;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                op = dictfetchall(cursor)
            # print(op)
            buy_id = int(op[0]['max']) + 1
            sell_id = int(op[0]['max']) + 2
            query = '''SELECT * from Customer where id=user_id;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = dictfetchall(cursor)
            new_value1 = user.balance - buyt2.price_per_share*buyt.num_shares
            new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
            new_value3 = user.invested_amount + buyt2.price_per_share*buyt.num_shares
            query2 = '''Update Customer SET balance = %s , current_value = %s , invested_amount = %s , (new_value1,new_value2,new_value3)'''
            with connection.cursor() as cursor:
                cursor.execute(query2)
            # sellt2.save()
            # buyt2.save()
            sql = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s)"
            sql2 = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s)"
            with connection.cursor() as cursor:
                cursor.execute(sql,val)
                connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(sql2,val1)
                connection.commit()
            
            sellt.num_shares -= buyt.num_shares
            heapq.heapreplace(sell_orders, (sellt.price_per_share, transaction))  
            # user_port = Portfolio.objects.get(customer=sellt.user_id,stock=sellt.stock_id)
            query='''SELECT * from Portfolio where customer=sellt.user_id and stock=sellt.stock_id'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user_port = dictfetchall(cursor)
            query1 = '''UPDATE Portfolio SET num_shares = %s, investes_amount = %s , current_value = %s WHERE customer = %s and stock = %s", (new_value1, new_value2, new_value3 , buyt.user_id , buyt.stock_id)'''     
            with connection.cursor() as cursor:
                cursor.execute(query1)
                connection.commit()
        else :
            heapq.heappop(buy_orders)
            heapq.heappop(sell_orders)
            query = '''SELECT max(id) FROM Transaction;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                op = dictfetchall(cursor)
            # print(op)
            buy_id = int(op[0]['max']) + 1
            sell_id = int(op[0]['max']) + 2
            query = '''SELECT * from Customer where id=user_id;'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = dictfetchall(cursor)
            new_value1 = user.balance - buyt2.price_per_share*buyt.num_shares
            new_value2 = user.current_value + buyt2.price_per_share*buyt.num_shares
            new_value3 = user.invested_amount + buyt2.price_per_share*buyt.num_shares
            query2 = '''Update Customer SET balance = %s , current_value = %s , invested_amount = %s , (new_value1,new_value2,new_value3)'''
            with connection.cursor() as cursor:
                cursor.execute(query2)
            # b_user_port = Portfolio.objects.get(customer=buyt.user_id,stock=buyt.stock_id)
            query = '''SELECT * from Portfolio where customer=buyt.user_id and stock=buyt.stock_id'''
            with connection.cursor() as cursor:
                cursor.execute(query)
                user_port = dictfetchall(cursor)
            with connection.cursor() as cursor:
                cursor.execute(query1)
                connection.commit()
            query1 = '''UPDATE Portfolio SET num_shares = %s, investes_amount = %s , current_value = %s WHERE customer = %s and stock = %s", (new_value1, new_value2,new_value3 , buyt.user_id , buyt.stock_id)'''
            
            # s_user_port = Portfolio.objects.get(customer=sellt.user_id,stock=sellt.stock_id)

            sql = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s)"
            sql2 = "INSERT INTO Transaction (id , customer , stock , date , num_shares , price_per_share , buy_or_sell) VALUES (%s, %s, %s , %s, %s, %s , %s)"
            with connection.cursor() as cursor:
                cursor.execute(sql,val)
                connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(sql2,val1)
                connection.commit()
            buyt.save()
            sellt.save()
            
    
    