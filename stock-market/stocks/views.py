from django.shortcuts import render
from django.http import HttpResponse
from .models import StockMetadata
def stocksview(request):
    return HttpResponse("Hello, Views to be seen here!")

def stocksall(request):
    stocks = StockMetadata.objects.all()
    return render (request, 'stock_details.html', {'stocks': stocks[0]})