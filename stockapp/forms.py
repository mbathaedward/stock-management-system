from django import forms
from .models import Stock,Category,StockHistory

#-------------------------------------------------------
#create a form here to directly update data in the model
#--------------------------------------------------------
class StockCreateform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category','item_name','quantity']

#validate category fields
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("This is field is required!")
        return category
#validate item_name fields
 
     
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        
        if not item_name:
            raise forms.ValidationError("This is field is required!")
        return item_name
    
# Cross-field validation: prevent duplicates
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        item_name = cleaned_data.get('item_name')

        if category and item_name:
             # Check if a Stock item with the same category + item_name already exists
             if Stock.objects.filter(category=category, item_name=item_name).exists():
                 raise forms.ValidationError(f"'{item_name}' already exist in '{category}'")
             return cleaned_data


#-------------------------------------------
# create a search form to search for products
# -------------------------------------------    
class StockSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    item_name = forms.CharField(required=False)
    class Meta:
        model = Stock
        fields = ['category','item_name']

class StockHistorySearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ['category','item_name','start_date','end_date']

class StockUpdateform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category','item_name','quantity']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issued_quantity', 'issue_to']

class ReceiveItem(forms.ModelForm):
    class Meta:
        model = Stock
        
        fields = ['received_quantity']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

