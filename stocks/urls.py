from django.urls import path
from django.urls import path, include, re_path
from . import views
import notifications.urls

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('stocks1', views.stocks_names, name='stocks_names'),
    path('stocks4',
         views.compare_2_stocks, name='compare_2_stocks'),
    path('stocks2', views.one_stock, name='one_stock'),
    path('stocks5', views.predict_prices, name='predict_prices'),
     path('stocks8', views.moving_avg, name='avg'),
    path('stocks3', views.stock_ret, name='stock_ret'),
    path('stocks6', views.stock_pnl, name='stock_pnl'),
     path('stocks9', views.top10, name='stock_top10'),
     path('stocks7', views.stock_roi, name='stock_roi'),
    path('register', views.registerPage, name='register'),
    
    path('logout', views.logoutPage, name='logout'),
    path('deregister', views.deregisterPage, name='deregister'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('users',views.user_names),
    path('transaction',views.trade_stock_view, name='transaction'),
    path('options',views.options, name='options'),
    path('buy_options',views.buy_options, name='buy_options'),
    path('futures',views.futures, name='futures'),
    path('buy_futures',views.buy_futures, name='buy_futures'),    
    path('success', views.success, name='success'),
    path('failure', views.failure, name='failure'),
    path('execute_options', views.execute_options, name='execute_options'),
    path('user_names', views.user_names, name='user_names'),
    path('q1', views.q1, name='q1'),
    path('q2', views.q2, name='q2'),
    path('q4', views.q4, name='q4'),
    path('stock_history', views.stock_history, name='stock_history'),
    path('stock_compare', views.compare_stocks, name='stock_compare'),
    path('profile', views.profile, name='profile'),
    path('funds', views.funds, name='funds'),
    path('holdings', views.holdings, name='holdings'),
    path('news_feed', views.news_feed, name='news_feed'),
    # re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),    
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
