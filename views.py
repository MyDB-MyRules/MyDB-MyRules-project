from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .forms import InputForm
from django.http import HttpResponseRedirect

from .models import StockHistory, StockMetadata
from .transactions import buy_stock 
from .forms import BuyForm

def dictfetchall(cursor):
    desc = cursor.description     
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def stocksview(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            stock_id = data['stock_id']
            return HttpResponseRedirect('stocks/' + str(stock_id))
    return render(request, 'dashboard.html', {})

def stocks_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select symbol from Stock_Metadata;''')
        stocks = dictfetchall(cursor)
    
    return render (request, 'stock_names.html', {'stocks': stocks})

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

def user_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select * from Customer;''')
        users = dictfetchall(cursor)
    
    return render (request, 'user_names.html', {'users': users})

def transaction(request):
    return render(request, 'transaction.html', {})

def buy_stock_view(request):
    # Ensure that the request is a POST request

    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            stock_id = data['stock_id']
    
    # Retrieve the user ID, stock ID, and quantity from the request
            user_id = data['user_id']
            stock_id = data['stock_id']
            quantity = data['quantity']

    # Retrieve the Stock object from the database
    stock = StockMetadata.objects.get(symbol=stock_id)

    # Call the buy_stock() function to perform the transaction
    # try:
    #     transaction = buy_stock(user_id, stock_id, quantity)
    # except ValueError as e:
    #     return HttpResponseBadRequest(str(e))
    transaction = buy_stock(user_id, stock_id, quantity)
    
    # Return a response to the user indicating that the transaction was successful
    return render(request, 'buy.html', {'transaction': transaction})