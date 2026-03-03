from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockCreateform

# Create your views here.
def home(requests):
    title = 'welcome: This is the home page'
    context = {
        'title': title

    }
    return render(requests, 'home.html', context)

def list_items(requests):
    title = 'List of list_items'
    queryset = Stock.objects.all()
    context = {
        'title': title,
        'queryset': queryset,
    }
    return render(requests, 'list_items.html',context)

def add_items(requests):
    form = StockCreateform(requests.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(requests, "add_items.html",  context)
        


