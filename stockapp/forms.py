from django import forms
from .models import Stock

#-------------------------------------------------------
#create a form here to directly update data in the model
#--------------------------------------------------------
class StockCreateform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category','item_name','quantity','issued_by']
    
