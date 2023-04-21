from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocksview, name='stocksview'),
    path('stocks1', views.stocks_names, name='stocks_names'),
    path('stocks4',
         views.compare_2_stocks, name='compare_2_stocks'),
    path('stocks2', views.one_stock, name='one_stock'),
    path('stocks5', views.predict_prices, name='predict_prices'),
     path('stocks8', views.moving_avg, name='avg'),
    path('stocks3', views.stock_ret, name='stock_ret'),
    path('stocks6',
         views.stock_pnl, name='stock_pnl'),
     path('stocks9', views.top10, name='stock_top10'),
     path('stocks7', views.stock_roi, name='stock_roi'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('deregister', views.deregisterPage, name='deregister'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('users',views.user_names),
    path('transaction',views.trade_stock_view),
]
