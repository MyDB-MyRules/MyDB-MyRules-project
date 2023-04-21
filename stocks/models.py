# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customer(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField()
    balance = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    current_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    invested_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Derivatives(models.Model):
    id = models.CharField(primary_key=True)
    buyer = models.ForeignKey(Customer, models.DO_NOTHING)
    seller = models.ForeignKey(Customer, models.DO_NOTHING, related_name='derivatives_seller_set')
    stock = models.ForeignKey('StockMetadata', models.DO_NOTHING)
    date = models.DateField()
    num_shares = models.DecimalField(max_digits=65535, decimal_places=65535)
    price_per_share = models.DecimalField(max_digits=65535, decimal_places=65535)
    buy_or_sell = models.BooleanField()
    execution_date = models.DateField()
    premium = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    derivative_type = models.CharField()

    class Meta:
        managed = False
        db_table = 'derivatives'


class Portfolio(models.Model):
    customer = models.OneToOneField(Customer, models.DO_NOTHING, primary_key=True)  # The composite primary key (customer_id, stock_id) found, that is not supported. The first column is selected.
    stock = models.ForeignKey('StockMetadata', models.DO_NOTHING)
    num_shares = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    invested_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    current_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portfolio'
        unique_together = (('customer', 'stock'),)


class StockHistory(models.Model):
    date = models.DateField(primary_key=True)  # The composite primary key (date, symbol) found, that is not supported. The first column is selected.
    symbol = models.ForeignKey('StockMetadata', models.DO_NOTHING, db_column='symbol')
    open = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    high = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    low = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    close = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    volume = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    turnover = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_history'
        unique_together = (('date', 'symbol'),)


class StockMetadata(models.Model):
    company_name = models.CharField()
    industry = models.CharField(blank=True, null=True)
    symbol = models.CharField(primary_key=True)
    isin_code = models.CharField()
    price_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_metadata'


class Transaction(models.Model):
    id = models.CharField(primary_key=True)
    buyer = models.ForeignKey(Customer, models.DO_NOTHING)
    seller = models.ForeignKey(Customer, models.DO_NOTHING, related_name='transaction_seller_set')
    stock = models.ForeignKey(StockMetadata, models.DO_NOTHING)
    date = models.DateField()
    num_shares = models.DecimalField(max_digits=65535, decimal_places=65535)
    price_per_share = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'transaction'


class Userdata(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    name = models.CharField()
    username = models.CharField(primary_key=True)
    email = models.CharField()
    password = models.CharField()

    class Meta:
        managed = False
        db_table = 'userdata'
