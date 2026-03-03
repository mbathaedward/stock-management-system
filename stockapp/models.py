from django.db import models

# Create your models here.

#---------------------
#stock table goes here
#---------------------
class Stock(models.Model):
    category = models.CharField(max_length=100, blank=True, null=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    recieve_quantity = models.IntegerField(default='0', blank=True, null=True)
    recieved_by = models.CharField(max_length=100, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issued_by = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateField(auto_now_add=False, auto_now=True)
    export_to_csv = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name}\n {self.quantity}"


