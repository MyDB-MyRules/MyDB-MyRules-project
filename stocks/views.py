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
from .forms import BuySellForm, CreateUserForm
from .transactions import trade_stock, buy_orders, sell_orders, transact

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


def one_stock(request, stock_id):
    with connection.cursor() as cursor:
        cursor.execute(
            '''select * from Stock_history where symbol = %s;''', [stock_id])
        stock = dictfetchall(cursor)

    return render(request, 'one_stock.html', {'stock': stock, 'stock_id': stock_id})


def stock_ret(request, stock_id):
    query = '''with a as (select row_number() over() as index, close from stock_history where symbol = %s), b as 
(select a1.close as close1, a2.close as close2, a1.index from a a1, a a2 where a1.index= a2.index-1)
select index,close2 - close1 as return from b;
;'''
    with connection.cursor() as cursor:
        cursor.execute(query, [stock_id])
        stock = dictfetchall(cursor)
    #print(stock)
    return render(request, 'stock_return.html', {'stock': stock, 'stock_id': stock_id})


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

    return render(request, 'stock_comp.html', {'stock': stock, 'stock_id1': stock_id1, 'stock_id2': stock_id2})


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
# check if relation has been updated
    with connection.cursor() as cursor:
        cursor.execute('select * from transaction;')
        print(dictfetchall(cursor))    
    return render(request, 'dashboard.html', {})

# predict prices


def predict_prices(request, stock_id):
    with connection.cursor() as cursor:
        cursor.execute(
            '''select * from past100prices where symbol = %s;''', [stock_id])
        stocks = dictfetchall(cursor)

    df = pd.DataFrame(stocks[len(stocks)-1])

    for i in range(len(stocks)-2, -1, -1):
        stock = stocks[i]
        df = df.append(stock, ignore_index=True)

    seriesdata = df.sort_index(ascending=True, axis=0)
    new_seriesdata = pd.DataFrame(index=range(
        0, len(df)), columns=['Date', 'Close'])
    length_of_data = len(seriesdata)
    for i in range(0, length_of_data):
        new_seriesdata['date'][i] = seriesdata['date'][i]
        new_seriesdata['close'][i] = seriesdata['close'][i]
    # setting the index again
    new_seriesdata.index = new_seriesdata.Date
    new_seriesdata.drop('Date', axis=1, inplace=True)
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


def moving_avg(request, stock_id):
    with connection.cursor() as cursor:
        cursor.execute(
            '''select sum(close)/30 from stock_history where symbol = %s order by date desc limit 30;''')
        val = dictfetchall(cursor)

    return render(request, 'avg.html', {'avg': val})

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