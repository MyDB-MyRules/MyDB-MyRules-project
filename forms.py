from django import forms
 
# creating a form
class BuyForm(forms.Form):
    user_id = forms.CharField()
    stock_id = forms.CharField()
    quantity = forms.DecimalField()
    buy_or_sell = forms.BooleanField(required=False)
    price = forms.DecimalField()
    MY_CHOICES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
    ]
    order = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter value'}), choices=MY_CHOICES)