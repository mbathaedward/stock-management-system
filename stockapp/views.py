from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockCreateform,StockSearchForm,StockUpdateform

# Create your views here.
def home(request):
    title = 'welcome: This is the home page'
    context = {
        'title': title

    }
    return render(request, 'home.html', context)

def list_items(request):
    header = 'List of list_items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    
    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category=form['category'].value(),
            item_name__icontains=form['item_name'].value()

        )
    context = {
        "header":header,
        "queryset":queryset,
        "form":form
    } 

    return render(request, 'list_items.html',context)

def add_items(request):
    form = StockCreateform(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request,'add_items.html',context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateform(instance=queryset)#create form with prefilled data of specific stock item
    if request.method == 'POST':
        form = StockUpdateform(request.POST,instance=queryset)#populate form with submitted data   

        if form.is_valid():
            form.save()  
            return redirect('/list_items')
    context = {
            'form':form
        }
    return render(request,'add_items.html',context)

def delete_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_items')
    return render(request, 'delete_item.html')
    


