from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    class CardStatuses(models.TextChoices):
        NOT_ACTIVE = 'NA', _('Не активована')
        ACTIVE = 'AC', _('Активована')
        OVERDUE = 'OD', _('Просрочена')

    serial_number = models.CharField(verbose_name="Серийный номер", max_length=2, blank=False, null=False, db_index=True)
    card_number = models.CharField(verbose_name="Номер карты", max_length=16, blank=False, null=False, db_index=True)
    release_date = models.DateTimeField(verbose_name="дата выпуска", auto_now=True)
    activity_end_date = models.DateTimeField(verbose_name='Дата окончания активности')
    cvv_code = models.CharField(verbose_name='CVV', max_length=3, blank=False, null=False)
    balance = models.FloatField(verbose_name='Сумма', default=0.00)
    card_status = models.CharField(verbose_name='Статус карты', choices=CardStatuses.choices,
                                   default=CardStatuses.NOT_ACTIVE, max_length=15)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        get_latest_by = ['release_date']
        abstract = False

    def get_absolute_url(self):
        return reverse('card_detail_url', kwargs={'card_number': self.card_number})

    def __str__(self):
        return self.card_number
