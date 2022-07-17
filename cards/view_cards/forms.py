from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from .models import Card

# class CardAdminForm(forms.ModelForm):
#     class Meta:
#         model = Card
#         fields = '__all__'
#
#     def clean_card_number(self):
#         new_card_number = self.cleaned_data['card_number']
#         if not new_card_number.isdigit():
#             raise ValidationError('Номер карти повинен складатися з цифр')
#         if 16 < len(new_card_number.strip()) > 16:
#             raise ValidationError('Номер карти повинен складатися з 16 цифр')
#         return new_card_number
#
#     def save(self, commit=None):
#         super(CardAdminForm, self).save(commit=False)
#         new_card_number = self.cleaned_data['card_number']
#
#         new_card = Card.objects.create(
#             serial_number=self.cleaned_data['serial_number'],
#             card_number=' '.join(new_card_number[i:i+4] for i in range(0, len(new_card_number), 4)),
#             activity_end_date=self.cleaned_data.get('release_data') + timedelta(days=365)
#                                  )
#         return new_card


class CardForm(forms.Form):
    activity_terms = (
        ('30', '1 місяць'),
        ('180', '6 місяців'),
        ('365', '1 рік')
    )

    serial_number = forms.CharField(label='Серійний номер: ', min_length=2, max_length=2)
    cards_count = forms.CharField(label='Кількість карток для генерації: ')
    activity_term = forms.ChoiceField(label='Термін дії картки: ', choices=activity_terms)

    def clean_serial_number(self):
        new__serial_number = self.cleaned_data['serial_number']
        if not new__serial_number.isdigit():
            raise ValidationError('Серійний номер повинен складатись з числа > 9')
        return new__serial_number

    def clean_cards_count(self):
        new_cards_count = self.cleaned_data['cards_count']
        try:
            if int(new_cards_count) >= 100:
                raise ValidationError('Згенерувати можна до 100 одиниць')
        except Exception:
            raise ValidationError('Кількість карток повинна бути числом > 0 и < 100')
        return new_cards_count

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'my_field'
