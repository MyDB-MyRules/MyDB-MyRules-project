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

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.id}, {self.name}, {self.balance}, {self.current_value}, {self.invested_amount})>'


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

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.customer}, {self.stock}, {self.num_shares}, {self.invested_amount}, {self.current_value})>'


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

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.date}, {self.symbol}, {self.open}, {self.high}, {self.low}, {self.close}, {self.volume}, {self.turnover})>'

class StockMetadata(models.Model):
    company_name = models.CharField()
    industry = models.CharField(blank=True, null=True)
    symbol = models.CharField(primary_key=True)
    isin_code = models.CharField()
    price_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_metadata'

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.company_name}, {self.industry}, {self.symbol}, {self.isin_code}, {self.price_per_share})>'


class Transaction(models.Model):
    id = models.CharField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    stock = models.ForeignKey(StockMetadata, models.DO_NOTHING)
    date = models.DateField()
    num_shares = models.DecimalField(max_digits=65535, decimal_places=65535)
    price_per_share = models.DecimalField(max_digits=65535, decimal_places=65535)
    buy_or_sell = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'transaction'

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.id}, {self.customer}, {self.stock}, {self.date}, {self.num_shares}, {self.price_per_share}, {self.buy_or_sell})>'

class Userdata(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    name = models.CharField()
    username = models.CharField(primary_key=True)
    email = models.CharField()
    password = models.CharField()

    class Meta:
        managed = False
        db_table = 'userdata'

    def __repr__(self):
        return f'<MyTable: MyTable object ({self.customer}, {self.name}, {self.username}, {self.email}, {self.password})>'