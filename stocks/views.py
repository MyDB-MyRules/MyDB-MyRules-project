from django.shortcuts import redirect, render
from django.http import HttpResponse
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

    return render(request, 'avg.html', {'avg': val})

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
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            register_user(username=username, password=password, customer_id=username +
                          '001', name=username, email=username + '@gmail.com')
            form.save()

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
    form2 = StockForm()
    form3 = StockRetForm()
    form4 = StockCompForm()
    form5 = StockPredictForm()
    form6 = Stockpnl()
    form7 = StockROI()
    form8 = StockAvg()
    form9 = StockTop10()
    return render(request, 'dashboard.html', {'form2':form2, 'form3':form3, 'form4':form4, 'form5':form5, 'form6':form6, 'form7':form7, 'form8':form8, 'form9':form9})

# predict prices


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
            '''select date, symbol, open, high, low, close, volume, turnover from past100prices where symbol = %s;''', [stock_id])
        stocks = dictfetchall(cursor)
    #print(stocks[len(stocks)-1])
    df = pd.DataFrame(stocks[0], index=[0])
    #print(df)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        df.loc[len(df.index)] = stock

    seriesdata = df.sort_index(ascending=True, axis=0)
    new_seriesdata = pd.DataFrame(index=range(
        0, len(df)), columns=['date', 'close'])
    length_of_data = len(seriesdata)

    print(new_seriesdata)
    for i in range(0, length_of_data):
        new_seriesdata['date'][i] = seriesdata['date'][i]
        new_seriesdata['close'][i] = seriesdata['close'][i]
    # setting the index again
    new_seriesdata.index = new_seriesdata.date
    new_seriesdata.drop('date', axis=1, inplace=True)
    # creating train and test sets this comprises the entire data’s present in the dataset
    myseriesdataset = new_seriesdata.values
    totrain = myseriesdataset[0:80, :]
    tovalid = myseriesdataset[80:, :]
    # converting dataset into x_train and y_train
    scalerdata = MinMaxScaler(feature_range=(0, 1))
    scale_data = scalerdata.fit_transform(myseriesdataset)
    x_totrain, y_totrain = [], []
    length_of_totrain = len(totrain)
    for i in range(60, length_of_totrain):
        x_totrain.append(scale_data[i-60:i, 0])
        y_totrain.append(scale_data[i, 0])
    x_totrain, y_totrain = np.array(x_totrain), np.array(y_totrain)
    x_totrain = np.reshape(
        x_totrain, (x_totrain.shape[0], x_totrain.shape[1], 1))
    # LSTM neural network
    lstm_model = Sequential()
    lstm_model.add(LSTM(units=50, return_sequences=True,
                   input_shape=(x_totrain.shape[1], 1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error', optimizer='adadelta')
    lstm_model.fit(x_totrain, y_totrain, epochs=3, batch_size=1, verbose=2)
    # predicting next data stock price
    myinputs = new_seriesdata[len(
        new_seriesdata) - (len(tovalid)+1) - 60:].values
    myinputs = myinputs.reshape(-1, 1)
    myinputs = scalerdata.transform(myinputs)
    tostore_test_result = []
    for i in range(60, myinputs.shape[0]):
        tostore_test_result.append(myinputs[i-60:i, 0])
    tostore_test_result = np.array(tostore_test_result)
    tostore_test_result = np.reshape(
        tostore_test_result, (tostore_test_result.shape[0], tostore_test_result.shape[1], 1))
    myclosing_priceresult = lstm_model.predict(tostore_test_result)
    myclosing_priceresult = scalerdata.inverse_transform(myclosing_priceresult)

    return render(request, 'predict.html', {'price': myclosing_priceresult})

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
            user_id = form.cleaned_data['user_id']
            stock_id = form.cleaned_data['stock_id']
            quantity = form.cleaned_data['quantity']
            buy_or_sell = form.cleaned_data['buy_or_sell']
            price = form.cleaned_data['price']
            order = form.cleaned_data['order']
            print(user_id, stock_id, quantity, buy_or_sell, price, order)
            # query = '''SELECT max(id) FROM Transaction;'''
            # with connection.cursor() as cursor:
            #     cursor.execute(query)
            #     op = dictfetchall(cursor)
            # # print(op)
            # num_id = int(op[0]['max']) + 1
            trade_stock(user_id, stock_id, quantity , buy_or_sell,price ,order)
            # Return a response to the user indicating that the transaction was successful
            # return render(request, 'buy_succesful.html')
    else:
        form = BuySellForm()
    
    return render(request , "transaction.html" , {"form" : form})

def options(request):
    form = OptionsForm()
    if request.method == 'POST':
        form = OptionsForm(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            trans_id = form.cleaned_data['trans_id']

            print(stock_id, trans_id)
            # insert option to derivatives table

    return render(request, 'options.html', {'options': options_buy, 'form': form})