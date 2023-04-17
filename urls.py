from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocksview, name='stocksview'),
    path('stocks/', views.stocks_names, name='stocks_names'),
    path('stocks/<str:stock_id1>,<str:stock_id2>',
         views.compare_2_stocks, name='compare_2_stocks'),
    path('stocks/<str:stock_id>', views.one_stock, name='one_stock'),
    path('stocks/predict/<str:stock_id>', views.predict_prices, name='predict_prices'),
    path('stocks/ret/<str:stock_id>', views.stock_ret, name='stock_ret'),
    path('stocks/pnl/<str:stock_id>,<str:doi>',
         views.stock_pnl, name='stock_pnl'),
    path('accounts/register', views.registerPage, name='register'),
    path('accounts/login', views.loginPage, name='login'),
    path('accounts/logout', views.logoutPage, name='logout'),
    path('accounts/deregister', views.deregisterPage, name='deregister'),
    path('accounts/dashboard', views.dashboard, name='dashboard'),
    
    
    
]
