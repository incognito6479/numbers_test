from django.contrib import admin
from mainapp.models import OrderDetail


@admin.register(OrderDetail)
class OrderDetailModelAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'price_usd', 'price_rub', 'delivery_date')
    search_fields = ('order_number',)
