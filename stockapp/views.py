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
    RecieveItem,
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
        instance.recieve_quantity = 0

        # Prevent issuing more than available
        if instance.issue_quantity > queryset.quantity:
            messages.error(
                request,
                f"Cannot issue {instance.issue_quantity} {queryset.item_name}(s). Only {queryset.quantity} left in store!"
            )
            return redirect('stock_detail', pk=queryset.id)

        # Reduce stock
        queryset.quantity -= instance.issue_quantity
        queryset.save()

        # Log to history
        StockHistory.objects.create(
            stock=queryset,
            issued_quantity=instance.issue_quantity,
            received_quantity=0,
            user=str(request.user)
        )

        messages.success(
            request,
            f"ISSUED SUCCESSFULLY. {queryset.quantity} {queryset.item_name}(s) now left in store"
        )
        return redirect('stock_detail', pk=queryset.id)

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    }
    return render(request, 'add_items.html', context)

# -----------------------
# RECEIVE ITEM
# -----------------------
@login_required
def recieve_item(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = RecieveItem(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0

        # Increase stock
        queryset.quantity += instance.recieve_quantity
        queryset.save()

        # Log to history
        StockHistory.objects.create(
            stock=queryset,
            issued_quantity=0,
            received_quantity=instance.recieve_quantity,
            user=str(request.user)
        )

        messages.success(
            request,
            f"RECEIVED SUCCESSFULLY. {queryset.quantity} {queryset.item_name}(s) now in store"
        )
        return redirect('stock_detail', pk=queryset.id)

    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": str(request.user)
    }
    return render(request, 'add_items.html', context)

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
    return render(request, 'list_history.html', {'header': header, 'queryset': queryset})