# Generated by Django 4.0.5 on 2022-06-27 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_orderdetail_price_rub_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order_numer',
            new_name='order_number',
        ),
    ]
