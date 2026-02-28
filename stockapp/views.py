from django.shortcuts import render
from .models import Stock

# Create your views here.
def home(requets):
    title = 'welcome: This is the home page'
    context = {
        'title': title

    }
    return render(requets, 'home.html', context)

def list_items(requets):
    title = 'List of list_items'
    queryset = Stock.objects.all()
    context = {
        'title': title,
        'queryset': queryset,
    }
    return render(requets, 'list_items.html',context)
