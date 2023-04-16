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
def trade_stock(user_id, stock_id, quantity , num_id , buy_or_sell,price ,order):
    # Get the user and stock objects
    user = Customer.objects.get(id=user_id)
    stock = StockMetadata.objects.get(symbol=stock_id)
    user_port = Portfolio.objects.get(customer=user_id,stock=stock_id)
    
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
        id=num_id,
        customer=user_id,
        stock=stock_id,
        date = today,
        num_shares=quantity,
        price_per_share =stock.price_per_share,
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
            buyt2.save()
            buyt.num_shares -= sellt.num_shares
            heapq.heapreplace(buy_orders, (-buyt.price_per_share, transaction))  
            user_port = Portfolio.objects.get(customer=buyt.user_id,stock=buyt.stock_id)
            #portfolio updation 
            
        elif buyt.num_shares<sellt.num_shares:
            sellt2 = sellt
            sellt2.num_shares = buyt.num_shares
            sellt2.price_per_share = buyt.price_per_share
            sellt2.save()
            sellt.num_shares -= buyt.num_shares
            heapq.heapreplace(sell_orders, (sellt.price_per_share, transaction))  
            user_port = Portfolio.objects.get(customer=sellt.user_id,stock=sellt.stock_id)
        else :
            heapq.heappop(buy_orders)
            heapq.heappop(sell_orders)
            b_user_port = Portfolio.objects.get(customer=buyt.user_id,stock=buyt.stock_id)
            s_user_port = Portfolio.objects.get(customer=sellt.user_id,stock=sellt.stock_id)
            buyt.save()
            sellt.save()
            
    
    