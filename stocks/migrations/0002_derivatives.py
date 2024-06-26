# Generated by Django 4.2 on 2023-04-21 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Derivatives',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('num_shares', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('price_per_share', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('buy_or_sell', models.BooleanField()),
                ('execution_date', models.DateField()),
                ('premium', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('derivative_type', models.CharField()),
            ],
            options={
                'db_table': 'derivatives',
                'managed': False,
            },
        ),
    ]
