from datetime import date
from django.db import connection
from .thread import *

def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def derivatives(buyer, seller, stock_id, num_shares, price_per_share,premium, execution_time):
    today = date.today()
    today = date.isoformat(today)
    
    query_togetid = '''select count(*) from derivatives;'''
    with connection.cursor() as cursor:
        cursor.execute(query_togetid)
        val = dictfetchall(cursor)
        print(val[0]['count'])

        query = '''insert into derivatives values(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)'''
        params = [val[0]['count'], buyer, seller,stock_id,today,num_shares,price_per_share,False,'2024-05-09',premium,'options']
    
    with connection.cursor() as cursor:
        cursor.execute(query,params)

    # start thread for sleeping
    print('done')
    t=CreateThread2(execution_time)
    t.start()
    # this will create new threads for each derivative done

