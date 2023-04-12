from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocksview, name='stocksview'),
    path('stocks/', views.stocks_names, name='stocks_names'),
    path('stocks/<str:stock_id1>,<str:stock_id2>', views.compare_2_stocks, name='compare_2_stocks'),
    path('stocks/<str:stock_id>', views.one_stock,name='one_stock'),
    path('stocks/ret/<str:stock_id>', views.stock_ret, name='stock_ret'),
    path('users',views.user_names),
    path('transaction',views.buy_stock_view),
]