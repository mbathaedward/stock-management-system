from django.db import models

category_choice = (
    ('Furniture','Furniture'),
    ('IT Equipment','IT Equipment'),
    ('Phone','Phone'),
    ('Electronics','Electronics'),
)

# Create your models here.

#---------------------
#stock table goes here
#---------------------

class Category(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name

class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    recieve_quantity = models.IntegerField(default=0, blank=True, null=True)
    recieved_by = models.CharField(max_length=100, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issued_by = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    export_to_csv = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.item_name} - {self.category  } - {self.quantity}"


