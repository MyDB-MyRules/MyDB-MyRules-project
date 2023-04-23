from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User 
 
# creating a form
class BuySellForm(forms.Form):
    stock_id = forms.CharField()
    quantity = forms.DecimalField()
    buy_or_sell = forms.BooleanField(required=False)
    price = forms.DecimalField(required=False)
    MY_CHOICES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
    ]
    order = forms.ChoiceField(choices=MY_CHOICES)
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StockForm(forms.Form):
    stock_id = forms.CharField()

class StockRetForm(forms.Form):
    stock_id = forms.CharField()

class StockCompForm(forms.Form):
    stock_id1 = forms.CharField()
    stock_id2 = forms.CharField()

class StockPredictForm(forms.Form):
    stock_id = forms.CharField()

class Stockpnl(forms.Form):
    stock_id = forms.CharField()
    doi = forms.DateField()

class StockROI(forms.Form):
    doi = forms.CharField()
    cutoffprofit = forms.DecimalField()

class StockAvg(forms.Form):
    stock_id = forms.CharField()

class StockTop10(forms.Form):
    doi = forms.DateField()
    

class OptionsForm(forms.Form):
    stock_id = forms.CharField()
    trans_id = forms.CharField()

class BuyOptionsForm(forms.Form):
    stock_id = forms.CharField()
    num_shares = forms.DecimalField()
    price_per_share = forms.DecimalField()
    premium = forms.DecimalField()
    execution_time = forms.DecimalField()