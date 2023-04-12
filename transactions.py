from django.db import transaction
from .models import Transaction, Portfolio , Customer , StockMetadata

@transaction.atomic()
def buy_stock(user_id, stock_id, quantity):
    # Get the user and stock objects
    user = Customer.objects.get(id=user_id)
    stock = StockMetadata.objects.get(symbol=stock_id)

    # Calculate the total cost of the transaction
    total_cost = quantity * stock.price_per_share

    # Check if the user has enough balance to buy the stock
    if user.balance < total_cost:
        raise ValueError("Not enough balance to buy this stock")

    # Create a new transaction object
    transaction = Transaction(
        user=user,
        stock=stock,
        quantity=quantity,
        price=stock.price,
        is_buy=True
    )

    # Update the user balance and stock quantity
    user.balance -= total_cost
    stock.quantity -= quantity

    # Save the changes to the database
    user.save()
    stock.save()
    transaction.save()
    return transaction 

# @transaction.atomic()
# def sell_stock(user_id, stock_id, quantity):
#     # Get the user and stock objects
#     user = User.objects.get(id=user_id)
#     stock = Stock.objects.get(id=stock_id)

#     # Check if the user has enough quantity of the stock to sell
#     if stock.quantity < quantity:
#         raise ValueError("Not enough quantity of this stock to sell")

#     # Calculate the total revenue of the transaction
#     total_revenue = quantity * stock.price

#     # Create a new transaction object
#     transaction = Transaction(
#         user=user,
#         stock=stock,
#         quantity=quantity,
#         price=stock.price,
#         is_buy=False
#     )

#     # Update the user balance and stock quantity
#     user.balance += total_revenue
#     stock.quantity += quantity

#     # Save the changes to the database
#     user.save()
#     stock.save()
#     transaction.save()
#     return transaction