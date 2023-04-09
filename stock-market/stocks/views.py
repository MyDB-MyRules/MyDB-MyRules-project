from django.shortcuts import render
from django.http import HttpResponse

def stocksview(request):
    return HttpResponse("Hello, Views to be seen here!")