from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class userregister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=255)  

    def __str__(self):
        return self.user.username


    
class adminregister(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()

    def __str__(self):
        return self.name
    


from django.contrib.auth.models import User

class ExpenseGroup(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')  # Use User model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class GroupMember(models.Model):
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=17)
    def __str__(self):
        return f'{self.name} - {self.phone_number}'
    def clean(self):
        if not self.phone_number.isdigit():
            raise ValidationError(_('Phone number must contain only digits'))


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, related_name='expenses')
    paid_by = models.ForeignKey(userregister, on_delete=models.CASCADE, related_name='paid_expenses')
    split_among = models.ManyToManyField(GroupMember, through='ExpenseSplit')
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)