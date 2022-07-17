from django.db import models
from view_cards.models import Card

class Check(models.Model):
    identifier = models.BigIntegerField(verbose_name='Номер чека', blank=False, null=False)
    date_of_purchase = models.DateTimeField(verbose_name='Дата покупки', auto_now=True)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, default=None)
    total_cost = models.IntegerField(verbose_name='Загальна ціна', default=0)

    def __str__(self):
        return self.identifier

class Product(models.Model):
    name = models.CharField(verbose_name='Название товара', max_length=50, blank=False, null=False)
    cost = models.PositiveIntegerField(verbose_name='Цена', blank=False, null=False)
    check_id = models.ForeignKey(Check, on_delete=models.CASCADE, verbose_name='Номер чека')

    def __str__(self):
        return self.name
