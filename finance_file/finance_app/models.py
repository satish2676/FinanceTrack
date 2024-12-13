from django.db import models
from datetime import datetime, timedelta
# Create your models here.
from django.db import models
import datetime
from datetime import date
from django.db import models





class Member(models.Model):
    loan_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    loan_disberment_amount = models.IntegerField()
    loan_date = models.DateField(auto_now_add=True)
    address = models.TextField()
    paid_amount = models.IntegerField()
    today_date = models.DateField(auto_now=True)
    
class Admin(models.Model):
    admin_name = models.CharField(max_length=100,default="s")
    admin_mobile = models.CharField(max_length=10,unique=True)
    admin_password = models.CharField(max_length=128)
    admin_code = models.CharField(default="satish123")
   



 

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    paid_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    today_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure today_date is always the current date when saving
        self.today_date = date.today()
        super().save(*args, **kwargs)
    