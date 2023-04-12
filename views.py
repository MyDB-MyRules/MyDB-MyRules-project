from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from .models import StockMetadata
from .transactions import buy_stock 
from .forms import BuyForm

def stocksview(request):
    return HttpResponse("Hello, Views to be seen here!")

def dictfetchall(cursor):
    desc = cursor.description     
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def stocks_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select symbol from Stock_Metadata;''')
        stocks = dictfetchall(cursor)
    
    return render (request, 'stock_names.html', {'stocks': stocks})

def user_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select * from Customer;''')
        users = dictfetchall(cursor)
    
    return render (request, 'user_names.html', {'users': users})


def one_stock(request, stock_id):
    with connection.cursor() as cursor:
        cursor.execute('''select * from Stock_history where symbol = %s;''', [stock_id])
        stock = dictfetchall(cursor)
    
    return render (request, 'one_stock.html', {'stock': stock, 'stock_id': stock_id})

def stock_ret(request, stock_id):
    query = '''with a as (select row_number() over() as index, close from stock_history where symbol = %s), b as 
(select a1.close as close1, a2.close as close2, a1.index from a a1, a a2 where a1.index= a2.index-1)
select index,close2 - close1 as return from b;
;'''
    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id])
        stock = dictfetchall(cursor)
    
    return render (request, 'stock_return.html', {'stock': stock, 'stock_id': stock_id})

def compare_2_stocks(request, stock_id1, stock_id2):
    query = '''with a as (select * from stock_history where symbol = %s), b as (select * from stock_history where symbol = %s) select a.date, a.close as close1, b.close as close2 from a, b where a.date = b.date; '''

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id1, stock_id2])
        stock = dictfetchall(cursor)
    
    return render (request, 'stock_comp.html', {'stock': stock, 'stock_id1': stock_id1, 'stock_id2': stock_id2})




def buy_stock_view(request):
    # Ensure that the request is a POST request
    # if request.method != 'POST':
    #     return HttpResponseBadRequest("Invalid request method")

    form = BuyForm(request.POST)
    
    # Retrieve the user ID, stock ID, and quantity from the request
    user_id = form.cleaned_data['user_id']
    stock_id = form.cleaned_data['stock_id']
    quantity = form.cleaned_data['quantity']

    # Retrieve the Stock object from the database
    stock = StockMetadata.objects.get(id=stock_id)

    # Call the buy_stock() function to perform the transaction
    # try:
    #     transaction = buy_stock(user_id, stock_id, quantity)
    # except ValueError as e:
    #     return HttpResponseBadRequest(str(e))
    transaction = buy_stock(user_id, stock_id, quantity)
    
    # Return a response to the user indicating that the transaction was successful
    return render(request, 'buy_success.html', {'transaction': transaction})

# def sell_stock_view(request):
#     # Ensure that the request is a POST request
#     if request.method != 'POST':
#         return HttpResponseBadRequest("Invalid request method")

#     # Retrieve the user ID, stock ID, and quantity from the request
#     user_id = request.POST.get('user_id')
#     stock_id = request.POST.get('stock_id')
#     quantity = int(request.POST.get('quantity'))

#     # Retrieve the Stock object from the database
#     stock = Stock.objects.get(id=stock_id)

#     # Call the sell_stock() function to perform the transaction
#     try:
#         transaction = sell_stock(user_id, stock_id, quantity)
#     except ValueError as e:
#         return HttpResponseBadRequest(str(e))

#     # Return a response to the user indicating that the transaction was successful
#     return render(request, 'sell_success.html', {'transaction': transaction})

