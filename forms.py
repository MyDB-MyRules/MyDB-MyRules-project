from django import forms
 
# creating a form
class BuyForm(forms.Form):
    user_id = forms.CharField()
    stock_id = forms.CharField()
    quantity = forms.DecimalField()
    