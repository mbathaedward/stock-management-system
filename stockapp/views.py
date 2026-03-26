from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockCreateform,StockSearchForm,StockUpdateform
from django.http import HttpResponse 
import csv
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import IssueForm,RecieveItem,ReorderLevelForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    title = 'welcome: This is the home page'
    context = {
        'title': title

    }
    return render(request, 'home.html', context)
@login_required
def list_items(request):
    header = 'List of list_items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    
    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category=form['category'].value(),
            item_name__icontains=form['item_name'].value()

        )
    if form['export_to_csv'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['content-Disposition'] = 'attachment; filename="LIst of Stock.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM NAME','QUANTITY'])
        instance = queryset
        for stock in instance:
            writer.writerow([stock.category,stock.item_name,stock.quantity])
        return response
    context = {
        "header":header,
        "queryset":queryset,
        "form":form
    } 

    return render(request, 'list_items.html',context)
@login_required
def add_items(request):
    form = StockCreateform(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "successfuly added items")
        return redirect('list_items')
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request,'add_items.html',context)
@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateform(instance=queryset)#create form with prefilled data of specific stock item
    if request.method == 'POST':
        form = StockUpdateform(request.POST,instance=queryset)#populate form with submitted data   

        if form.is_valid():
            form.save()  
            messages.success(request, "succesfully updated")
            return redirect('/list_items')
    context = {
            'form':form
        }
    return render(request,'add_items.html',context)
@login_required
def delete_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, "Deleted succesfully")
        return redirect('/list_items')
    return render(request, 'delete_item.html')

def stock_detail(request,pk):
    queryset = get_object_or_404(Stock, id=pk)
    context = {
        'queryset':queryset,
    }
    return render(request, 'stock_detail.html',context)




def issue_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = IssueForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)

        # Reduce quantity
        instance.quantity -= instance.issue_quantity

        # instance.issue_by = str(request.user)

        instance.save()

        messages.success(
            request,
            f"ISSUED SUCCESSFULLY. {instance.quantity} {instance.item_name}(s) now left in store"
        )

        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    }

    return render(request, 'add_items.html', context)


def recieve_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = IssueForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)

        # Increase quantity
        instance.quantity += instance.issue_quantity

        instance.issue_by = str(request.user)
        instance.save()

        messages.success(
            request,
            f"RECEIVED SUCCESSFULLY. {instance.quantity} {instance.item_name}(s) now in store"
        )

        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    }

    return render(request, 'add_items.html', context)


def reorder_level(request,pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = ReorderLevelForm(request.POST or None,instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Reorder level " + str(instance.item_name) +  "is updated to" + str(instance.reorder_level) )
        return redirect("/list_items")
    context = {
        "instance":queryset,
        "form":form
    }
    return render(request, "add_items.html", context)

    
    


    

       
  
    
    


