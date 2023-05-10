from datetime import date
from django.db import connection
from .thread import *

def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def derivatives(request, buyer, seller, stock_id, num_shares, price_per_share,premium, execution_time, type):
    today = date.today()
    today = date.isoformat(today)
    
    query_togetid = '''select count(*) from derivatives;'''
    with connection.cursor() as cursor:
        cursor.execute(query_togetid)
        val = dictfetchall(cursor)
        id = val[0]['count']

    query = '''select id from customer where name = %s;'''
    with connection.cursor() as cursor:
        cursor.execute(query, [buyer])
        val = dictfetchall(cursor)
        buyer_id = val[0]['id']
    
    with connection.cursor() as cursor:
        cursor.execute(query, [seller])
        val = dictfetchall(cursor)
        seller_id = val[0]['id']

    query = '''insert into derivatives values(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);'''
    params = [id, buyer_id, seller_id,stock_id,today,num_shares,price_per_share,execution_time,premium,type]

    with connection.cursor() as cursor:
        cursor.execute(query,params)

    # start thread for sleeping
    print('done')
    
    if type == 'futures':
        t=FuturesThread(request, execution_time, params, buyer, seller)
    else:
        t=OptionsThread(request, execution_time, params, buyer, seller)
        
    t.start()
    # this will create new threads for each derivative done

