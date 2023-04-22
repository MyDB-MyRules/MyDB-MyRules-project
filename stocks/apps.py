from django.apps import AppConfig
from .thread import *

class StocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks'
    
    def ready(self) -> None:
        from .transactions import transact
        t = CreateThread(transact)
        t.start()
        return super().ready()