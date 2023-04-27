from django.apps import AppConfig
from .thread import *

class StocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks'
    
    def ready(self) -> None:
        from .transactions import transact
        from .views import register_marketmaker
        
        register_marketmaker()
        
        # create a thread to run the transaction manager
        t = CreateThread1(transact)
        # die when the main thread dies 
        t.daemon = True 
        t.start()
        return super().ready()