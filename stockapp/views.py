from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv

from .models import Stock, StockHistory
from .forms import (
    StockCreateform,
    StockSearchForm,
    StockUpdateform,
    IssueForm,
    ReceiveItem,
    ReorderLevelForm
)

# -----------------------
# HOME PAGE
# -----------------------
def home(request):
    context = {'title': 'Welcome: This is the home page'}
    return render(request, 'home.html', context)

# -----------------------
# LIST ITEMS
# -----------------------
@login_required
def list_items(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()

    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )

    # Export CSV
    if form['export_to_csv'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="List_of_Stock.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
        for stock in queryset:
            writer.writerow([stock.category, stock.item_name, stock.quantity])
        return response

    context = {
        "header": header,
        "queryset": queryset,
        "form": form
    }
    return render(request, 'list_items.html', context)

# -----------------------
# ADD ITEM
# -----------------------
@login_required
def add_items(request):
    form = StockCreateform(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully added item")
        return redirect('list_items')
    return render(request, 'add_items.html', {'form': form, 'title': 'Add Item'})

# -----------------------
# UPDATE ITEM
# -----------------------
@login_required
def update_items(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = StockUpdateform(instance=queryset)

    if request.method == 'POST':
        form = StockUpdateform(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated item")
            return redirect('list_items')

    return render(request, 'add_items.html', {'form': form})

# -----------------------
# DELETE ITEM
# -----------------------
@login_required
def delete_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, "Deleted successfully")
        return redirect('list_items')
    return render(request, 'delete_item.html', {'queryset': queryset})

# -----------------------
# STOCK DETAIL
# -----------------------
@login_required
def stock_detail(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    return render(request, 'stock_detail.html', {'queryset': queryset})

# -----------------------
# ISSUE ITEM
# -----------------------
@login_required
def issue_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = IssueForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.received_quantity = 0

        # Prevent issuing more than available
        if instance.issued_quantity > queryset.quantity:
            messages.error(
                request,
                f"Cannot issue {instance.issued_quantity} {queryset.item_name}(s). Only {queryset.quantity} left!"
            )
            return redirect('stock_detail', pk=queryset.id)

        # Reduce stock
        queryset.quantity -= instance.issued_quantity
        queryset.issued_quantity = instance.issued_quantity
        queryset.issued_by = str(request.user)
        queryset.save()

        # Log history
        StockHistory.objects.create(
            category=queryset.category,
            item_name=queryset.item_name,
            quantity=queryset.quantity,
            issued_quantity=instance.issued_quantity,
            received_quantity=0,
            issued_by=str(request.user),
            issue_to=instance.issue_to,
        )

        messages.success(
            request,
            f"ISSUED SUCCESSFULLY. {queryset.quantity} left in store"
        )
        return redirect('stock_detail', pk=queryset.id)

    return render(request, 'add_items.html', {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    })

# -----------------------
# RECEIVE ITEM
# -----------------------
@login_required
def receive_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = ReceiveItem(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.issued_quantity = 0

        #Increase stock
        queryset.quantity += instance.received_quantity
        queryset.received_quantity = instance.received_quantity
        queryset.received_by = str(request.user)
        queryset.save()

        # Log history
        StockHistory.objects.create(
            category=queryset.category,
            item_name=queryset.item_name,
            quantity=queryset.quantity,
            issued_quantity=0,
            received_quantity=instance.received_quantity,
            received_by=str(request.user),
        )

        messages.success(
            request,
            f"RECEIVED SUCCESSFULLY. {queryset.quantity} now in store"
        )
        return redirect('stock_detail', pk=queryset.id)

    return render(request, 'add_items.html', {
        "title": 'Receive ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    })

# -----------------------
# REORDER LEVEL
# -----------------------
@login_required
def reorder_level(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(
            request,
            f"Reorder level for {instance.item_name} updated to {instance.reorder_level}"
        )
        return redirect('list_items')

    return render(request, 'add_items.html', {'form': form, 'instance': queryset})

# -----------------------
# LIST HISTORY
# -----------------------
@login_required
def list_history(request):
    header = 'List of Stock History'
    queryset = StockHistory.objects.all()            
    form = StockSearchForm(request.POST or None)
    
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        if (category !=''):
            queryset = queryset.filter(category_id=category)
    context = {
                "form":form,
                "header":header,
                "queryset":queryset
            }
               
            


    return render(request, 'list_history.html', context)