import copy
import time
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from .forms import *
from .transactions import trade_stock, buy_orders, sell_orders, transact, options_buy
from .derivatives import derivatives
from django.contrib import messages
from .thread import options_to_execute

def stocksview(request):
    return HttpResponse("Hello, Views to be seen here!")


def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def stocks_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select symbol from Stock_Metadata;''')
        stocks = dictfetchall(cursor)

    return render(request, 'stock_names.html', {'stocks': stocks})


def one_stock(request):
    # Ensure that the request is a POST request
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id = form.cleaned_data['stock_id']
                
    with connection.cursor() as cursor:
        cursor.execute(
            '''select * from Stock_history where symbol = %s;''', [stock_id])
        stock = dictfetchall(cursor)

    return render(request, 'one_stock.html', {'stock': stock, 'stock_id': stock_id})


def stock_ret(request):
    query = '''with a as (select row_number() over() as index, close from stock_history where symbol = %s), b as 
(select a1.close as close1, a2.close as close2, a1.index from a a1, a a2 where a1.index= a2.index-1)
select index,close2 - close1 as return from b;
;'''
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockRetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id = form.cleaned_data['stock_id']

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id])
        stock = dictfetchall(cursor)
    #print(stock)
    return render(request, 'stock_return.html', {'stock': stock, 'stock_id': stock_id})


def stock_pnl(request):
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
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Stockpnl(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id = form.cleaned_data['stock_id']
            doi = form.cleaned_data['doi']

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id, doi, stock_id])
        stock = dictfetchall(cursor)

    # return render (request, 'stock_return.html', {'stock': stock, 'stock_id': stock_id})
    return HttpResponse(stock[0]['pnl'])

def stock_roi(request):
    query = """
    with old as 
    (
        select symbol, close 
        from stock_history
        where date = %s
    ), 
    latest as 
    (
        select symbol, close, date 
        from stock_history
        order by date desc
        limit 1
    ), 
    pnl as 
    (    
        select old.symbol, 
            ((latest.close - old.close) / old.close) * 100 as pnl 
        from old, latest
        where old.symbol = latest.symbol
    )

    select * from pnl where pnl > %s;    
    """
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockROI(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            doi = form.cleaned_data['doi']
            cutoff = form.cleaned_data['cutoffprofit']

    with connection.cursor() as cursor:
        cursor.execute(query, [doi, cutoff])
        stock = dictfetchall(cursor)

    return render(request, 'roi.html', {'stocks' : stock})

def compare_2_stocks(request):
    query = '''with a as (select * from stock_history where symbol = %s), b as (select * from stock_history where symbol = %s) select a.date, a.close as close1, b.close as close2 from a, b where a.date = b.date; '''
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockCompForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id1 = form.cleaned_data['stock_id1']
            stock_id2 = form.cleaned_data['stock_id2']

    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id1, stock_id2])
        stock = dictfetchall(cursor)

    return render(request, 'stock_comp.html', {'stock': stock, 'stock_id1': stock_id1, 'stock_id2': stock_id2})

def moving_avg(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockRetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id = form.cleaned_data['stock_id']

    with connection.cursor() as cursor:
        cursor.execute(
            '''
        with a as 
        (
        SELECT * from  stock_history
        WHERE symbol = %s ORDER BY date DESC
        LIMIT 30
        )
        SELECT AVG(close)
        FROM a group by symbol;''', [stock_id])
        val = dictfetchall(cursor)

    return render(request, 'avg.html', {'avg': val[0]['avg']})

def top10(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockTop10(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            doi = form.cleaned_data['doi']

    with connection.cursor() as cursor:
        cursor.execute(
            '''    with old as 
    (
        select symbol, close 
        from stock_history
        where date = %s
    ), 
    latest as 
    (
        select distinct on (symbol) symbol, close, date 
        from stock_history
        order by symbol, date desc
    ) 
    select old.symbol, 
        ((latest.close - old.close) / old.close) * 100 as pnl 
    from old, latest
    where old.symbol = latest.symbol
    order by pnl desc
    limit 10;
''', [doi])
        val = dictfetchall(cursor)

    return render(request, 'top10.html', {'top10': val})

def register_marketmaker():
    
    with connection.cursor() as cursor:
        cursor.execute('select 1 from customer where id = 0::varchar;')
        output = dictfetchall(cursor)

    if len(output) == 0:
        query = '''
        insert into 
            customer(id, name, balance)
        VALUES (%s, %s, %s);
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query, [0, 'marketmaker', 1000000000])

def register_user(username, password, name, email):
    
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from customer;')
        output = dictfetchall(cursor)
        customer_id = output[0]['count'] + 1  
    
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
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            register_user(username=username, password=password, name=username, email=email)
            form.save()
            messages.success(request, 'User registered successfully')  

            return redirect('login')

    context = {'form': form}
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
    if(len(options_to_execute) != 0):
        messages.success(request, 'Your option has been executed. Please accept the transaction by proceeding to the accept_options page.')
    
    query0  = '''select id from customer where name = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query0, [request.user.username])
        id = dictfetchall(cursor)[0]['id']

    query = '''select * from portfolio where customer_id = %s and num_shares > 0;'''
    with connection.cursor() as cursor:
        cursor.execute(query, [id])
        portfolio = dictfetchall(cursor)
        
    return render(request, 'dashboard.html', {'portfolio' : portfolio})
# predict prices

def q1(request):
    form5 = StockPredictForm()
    form6 = Stockpnl()
    form7 = StockROI()
    form8 = StockAvg()
    form9 = StockTop10()

    return render(request, 'q1.html', {'form5':form5, 'form6':form6, 'form7':form7, 'form8':form8, 'form9':form9})

def q2(request):
    form2 = StockForm()
    form4 = StockCompForm()

    return render(request, 'q2.html', {'form2':form2, 'form4':form4})

def q4(request):
    return render (request, 'q4.html', {})

def predict_prices(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = StockRetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            
            stock_id = form.cleaned_data['stock_id']

    with connection.cursor() as cursor:
        cursor.execute(
            '''select date, close from past100prices where symbol = %s;''', [stock_id])
        stocks = dictfetchall(cursor)
    #print(stocks[len(stocks)-1])
    df = pd.DataFrame(stocks[0], index=[0])
    #print(df)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        df.loc[len(df.index)] = stock

    training_set = df.iloc[:, 1:2].values
    sc = MinMaxScaler(feature_range=(0,1))
    training_set_scaled = sc.fit_transform(training_set)

    X_train = []
    y_train = []
    for i in range(5, 100):
        X_train.append(training_set_scaled[i-5:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


    from keras.models import Sequential
    from keras.layers import LSTM
    from keras.layers import Dropout
    from keras.layers import Dense

    model = Sequential()
    model.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam',loss='mean_squared_error')



    model.fit(X_train,y_train,epochs=10,batch_size=8)
    predicted_stock_price = model.predict(X_train[94])
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    return render(request, 'predict.html', {'price': predicted_stock_price[0]})

def user_names(request):
    with connection.cursor() as cursor:
        cursor.execute('''select * from Customer;''')
        users = dictfetchall(cursor)
    
    return render (request, 'user_names.html', {'users': users})

def trade_stock_view(request):
    # Ensure that the request is a POST request
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = BuySellForm(request.POST)
        # check whether it's valid:
        if form.is_valid():   
            # Retrieve the user ID, stock ID, and quantity from the request
            user_name =request.user.username
            stock_id = form.cleaned_data['stock_id']
            quantity = form.cleaned_data['quantity']
            buy_or_sell = form.cleaned_data['buy_or_sell']
            price = form.cleaned_data['price']
            order = form.cleaned_data['order']
            print(user_name, stock_id, quantity, buy_or_sell, price, order)
            # query = '''SELECT max(id) FROM Transaction;'''
            # with connection.cursor() as cursor:
            #     cursor.execute(query)
            #     op = dictfetchall(cursor)
            # # print(op)
            # num_id = int(op[0]['max']) + 1
            trade_stock(user_name, stock_id, quantity , buy_or_sell,price ,order)
            # Return a response to the user indicating that the transaction was successful
            return redirect('success')
    else:
        form = BuySellForm()
    
    return render(request , "transaction.html" , {"form" : form})

def options(request):
    
    if request.method == 'POST':
        form = OptionsForm(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            trans_id = int(form.cleaned_data['trans_id'])
            
            buyer = options_buy[stock_id][trans_id][0]
            seller = request.user.username
            num_shares = options_buy[stock_id][trans_id][1]
            price_per_share = options_buy[stock_id][trans_id][2]
            premium = options_buy[stock_id][trans_id][3]
            execution_time = options_buy[stock_id][trans_id][4]
            
            # request_copy = copy.copy(request)
            derivatives(request,buyer,seller,stock_id, num_shares,price_per_share, premium, execution_time)     
            # messages.warning(request, 'Transaction Successful')
            return redirect('success')
    else:
        form = OptionsForm()
    
    options_avail = {}
    for (symbol, orders) in options_buy.items():
        if(len(orders) != 0):
            options_avail[symbol] = orders
            
    return render(request, 'options.html', {'options': options_avail, 'form': form})

def buy_options(request):
    if request.method == 'POST':
        form = BuyOptionsForm(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            num_shares = float(form.cleaned_data['num_shares'])
            price_per_share = float(form.cleaned_data['price_per_share'])
            premium = float(form.cleaned_data['premium'])
            execution_time = float(form.cleaned_data['execution_time'])
            user= request.user.username
            options_buy[stock_id].append((user, num_shares, price_per_share, premium, execution_time))
            return redirect('success')
    else:
        form = BuyOptionsForm()
    return render(request, 'buy_options.html', {'form':form})

def execute_options(request):
    
    if request.method == 'POST':
        form = ExecuteOptionsForm(request.POST)
        if form.is_valid():
            user_name = request.user.username
            sno = int(form.cleaned_data['sno'])

            print('sno = %s', sno)    
            txn = options_to_execute[sno - 1]
            options_to_execute.pop(sno - 1)
            
            print('txn = %s', txn)
            # txn = [id, buyer_id, seller_id,stock_id,today,num_shares,price_per_share,5,premium,'options']
            
            stock_id = txn[3]
            quantity = txn[5]
            buy_or_sell = True
            price = txn[6]
            order = 'limit'  
                    
            trade_stock(user_name, stock_id, quantity , buy_or_sell,price ,order)
                    
            return redirect('success')  
    else:
        form = ExecuteOptionsForm()
            
    return render(request, 'execute_options.html', {'options': options_to_execute, 'form': form})

def success(request):
    return render(request, 'success.html')


def stock_history(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            query1 = '''SELECT * from Stock_history where symbol=%s LIMIT 100;'''        
            with connection.cursor() as cursor:
                cursor.execute(query1,[stock_id])
                stock_history = dictfetchall(cursor)

            dates = [entry['date'].strftime('%Y-%m-%d') for entry in stock_history]
            opens = [entry['open'] for entry in stock_history]
            highs = [entry['high'] for entry in stock_history]
            lows = [entry['low'] for entry in stock_history]
            closes = [entry['close'] for entry in stock_history]
            volumes = [entry['volume'] for entry in stock_history]
            turnovers = [entry['turnover'] for entry in stock_history]
            context = {
                'stock_id': stock_id,
                'dates': dates,
                'opens': opens,
                'highs': highs,
                'lows': lows,
                'closes': closes,
                'volumes': volumes,
                'turnovers': turnovers,
            }
            return render(request, 'history.html', context)
    else:
        form = HistoryForm()
            
    return render(request, 'history_form.html', {'form': form})

def compare_stocks(request):
    if request.method == 'POST':
        form = StockCompForm(request.POST)
        if form.is_valid():
            stock_id1 = form.cleaned_data['stock_id1']
            stock_id2 = form.cleaned_data['stock_id2']
            query1 = '''SELECT * from Stock_history where symbol=%s LIMIT 100;'''        
            with connection.cursor() as cursor:
                cursor.execute(query1,[stock_id1])
                stock_history1 = dictfetchall(cursor)
            with connection.cursor() as cursor:
                cursor.execute(query1,[stock_id2])
                stock_history2 = dictfetchall(cursor)
            dates = [entry['date'].strftime('%Y-%m-%d') for entry in stock_history1]
            opens = [entry['open'] for entry in stock_history1]
            highs = [entry['high'] for entry in stock_history1]
            lows = [entry['low'] for entry in stock_history1]
            closes = [entry['close'] for entry in stock_history1]
            volumes = [entry['volume'] for entry in stock_history1]
            turnovers = [entry['turnover'] for entry in stock_history1]
            
            dates2 = [entry['date'].strftime('%Y-%m-%d') for entry in stock_history2]
            opens2 = [entry['open'] for entry in stock_history2]
            highs2 = [entry['high'] for entry in stock_history2]
            lows2 = [entry['low'] for entry in stock_history2]
            closes2 = [entry['close'] for entry in stock_history2]
            volumes2 = [entry['volume'] for entry in stock_history2]
            turnovers2 = [entry['turnover'] for entry in stock_history2]
            context = {
                'stock_id1': stock_id1,
                'dates': dates,
                'opens': opens,
                'highs': highs,
                'lows': lows,
                'closes': closes,
                'volumes': volumes,
                'turnovers': turnovers,
                'stock_id2': stock_id2,
                'dates2': dates2,
                'opens2': opens2,
                'highs2': highs2,
                'lows2': lows2,
                'closes2': closes2,
                'volumes2': volumes2,
                'turnovers2': turnovers2,
            }
            # print(context)
            return render(request, 'compare.html', context)
        
    else:
        form = StockCompForm()
            
    return render(request, 'compare_form.html', {'form': form})