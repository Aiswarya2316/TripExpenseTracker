from django import forms
from .models import MemberBudget

class MemberBudgetForm(forms.ModelForm):
    class Meta:
        model = MemberBudget
        fields = ['member', 'group', 'total_spent']
