from django import forms
 
# creating a form
class BuySellForm(forms.Form):
    user_id = forms.CharField()
    stock_id = forms.CharField()
    quantity = forms.DecimalField()
    buy_or_sell = forms.BooleanField(required=False)
    price = forms.DecimalField(required=False)
    MY_CHOICES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
    ]
    order = forms.ChoiceField(choices=MY_CHOICES)