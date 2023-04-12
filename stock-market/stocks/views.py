from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout

from .models import StockMetadata

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


def stock_pnl(request, stock_id, doi):
    query = """
    with old as 
    (
        select close 
        from stock_history
        where symbol = %s
            and date = %s
    ), 
    latest as 
    (
        select close, date 
        from stock_history
        where symbol = %s
        order by date desc
        limit 1
    ) 
    select ((latest.close - old.close) / old.close) * 100 as pnl 
    from old, latest;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id, doi, stock_id])
        stock = dictfetchall(cursor)
    
    print(stock)
    # return render (request, 'stock_return.html', {'stock': stock, 'stock_id': stock_id})
    return HttpResponse(stock[0]['pnl'])



def compare_2_stocks(request, stock_id1, stock_id2):
    query = '''with a as (select * from stock_history where symbol = %s), b as (select * from stock_history where symbol = %s) select a.date, a.close as close1, b.close as close2 from a, b where a.date = b.date; '''

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id1, stock_id2])
        stock = dictfetchall(cursor)
    
    return render (request, 'stock_comp.html', {'stock': stock, 'stock_id1': stock_id1, 'stock_id2': stock_id2})

def register_user(username, password, customer_id, name, email):
    query = '''
    insert into 
        customer(id, name, balance)
    VALUES (%s, %s, %s);
    '''

    init_balance = 50000 
    with connection.cursor() as cursor:
        cursor.execute(query, [customer_id, name, init_balance])

# # check if relation has been updated
#     with connection.cursor() as cursor:
#         cursor.execute('select * from customer;')
#         print(dictfetchall(cursor))

    query = '''
    insert into 
        userdata(username, password, customer_id, name, email)
    VALUES (%s, %s, %s, %s, %s);
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [username, password, customer_id, name, email])

# # check if relation has been updated
#     with connection.cursor() as cursor:
#         cursor.execute('select * from userdata;')
#         print(dictfetchall(cursor))    

def deregister_user(username):
    query = '''
    delete from userdata
    where userdata.username = %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [username])

# check if relation has been updated
    with connection.cursor() as cursor:
        cursor.execute('select * from userdata;')
        print(dictfetchall(cursor))    

def auth_user(username, password):
    query = '''
    select customer_id 
    from userdata a
    where a.username = %s 
        and a.password = %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [username, password])
        output = dictfetchall(cursor)

    return len(output) > 0 
    
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            register_user(username=username, password=password, customer_id=username + '001', name=username, email=username + '@gmail.com')
            form.save()

            return redirect('login')

    context = {'form' : form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        verified = auth_user(username, password)

        if verified and user is not None:
            login(request, user)
            return redirect('dashboard')
        # else:
        #     messages.info(request, 'Incorrect credentials')

    context = {}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def deregisterPage(request):
    username = str(request.user)
    print(username)
    deregister_user(username)
    return redirect('register')

def dashboard(request):
    return render(request, 'dashboard.html', {})