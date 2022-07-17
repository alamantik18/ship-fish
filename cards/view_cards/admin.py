from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Card

@admin.register(Card)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('card_number', )

admin.site.unregister(Group)
