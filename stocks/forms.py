from django import forms
 
# creating a form
class BuySellForm(forms.Form):
    user_id = forms.CharField()
    stock_id = forms.CharField()
    quantity = forms.DecimalField()
    buy_or_sell = forms.BooleanField(required=False)
    price = forms.DecimalField()
    premium = forms.BooleanField(required=False)
    MY_CHOICES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
        ('stop', 'Stop Order'),
        ('option', 'Option'),
        ('future', 'Future'),
    ]
    order = forms.ChoiceField(choices=MY_CHOICES)