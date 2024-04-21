from django import forms
from .models import IncomeExpense


class IncomeExpenseForm(forms.ModelForm):
    class Meta:
        model = IncomeExpense
        fields = ['amount', 'description', 'date', 'category', 'type']
