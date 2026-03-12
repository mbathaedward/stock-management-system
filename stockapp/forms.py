from django import forms
from .models import Stock

#-------------------------------------------------------
#create a form here to directly update data in the model
#--------------------------------------------------------
class StockCreateform(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ['category','item_name','quantity']


    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("This is field is required!")
 #check if category exist       
        for instance in Stock.objects.all():
            if instance.category == category:
                raise forms.ValidationError(category + "is already created")

        return category
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        
        if not item_name:
            raise forms.ValidationError("This is field is required!")
        return item_name






#-------------------------------------------
# create a search form to search for products
# -------------------------------------------    
class StockSearchForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category','item_name']

class StockUpdateform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category','item_name','quantity']