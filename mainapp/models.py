from django.db import models


class OrderDetail(models.Model):
    id_from_sheet = models.IntegerField(unique=True, verbose_name="Порядок заказа в листе")
    order_number = models.BigIntegerField(verbose_name="Номер заказа")
    price_usd = models.IntegerField(verbose_name="Стоимость в долларах")
    price_rub = models.IntegerField(verbose_name="Стоимость в рублях")
    delivery_date = models.DateField(verbose_name="Срок поставки")

    def __str__(self):
        return f"{self.order_number} | {self.delivery_date}"

    class Meta:
        verbose_name = "Подробности заказа"
        verbose_name_plural = "Детали заказов"
