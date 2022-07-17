from django.shortcuts import redirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .forms import CardForm
from .models import Card
from checks.models import *

import datetime
import random
import string


def generate_string(length):
    return ''.join(random.choices(string.digits, k=length))


def get_activity_end_date(start_date, active_term):
    date = start_date
    date += datetime.timedelta(days=int(active_term))
    return date


def cards_list(request):
    if request.method == 'POST' and 'create_cards' in request.POST:
        form = CardForm(request.POST)
        if form.is_valid():
            card_statuses = ['Не активована', 'Активована']

            objs_cards = [
                Card(
                    serial_number=form.cleaned_data['serial_number'],
                    card_number=' '.join(generate_string(16)[i:i + 4] for i in range(0, 16, 4)),
                    activity_end_date=get_activity_end_date(datetime.now(), form.cleaned_data['activity_term']),
                    cvv_code=generate_string(3),
                    balance=random.randint(100, 100000),
                    card_status=random.choice(card_statuses)
                )
                for _ in range(int(form.cleaned_data['cards_count']))
            ]
            msg = Card.objects.bulk_create(objs_cards)
            message = 'Записи згенеровано'
            messages.info(request, message=message)
            return redirect('/')
    else:
        form = CardForm()
    if request.method == 'POST' and 'delete-card' in request.POST:
        card = Card.objects.get(card_number=request.POST['delete-card'])
        card.delete()
        message = 'Запис видалено'
        messages.info(request, message=message)

    search_query = request.GET.get('search', '')

    now = datetime.datetime.now()
    for card in Card.objects.all():
        if now > card.activity_end_date:
            Card.objects.filter(card_number=card.card_number).update(card_status='Просрочена')

    cards = Card.objects.filter(
        Q(serial_number__icontains=search_query) |
        Q(card_number__icontains=search_query) |
        Q(release_date__icontains=search_query) |
        Q(activity_end_date__icontains=search_query) |
        Q(card_status__icontains=search_query)
    ) if search_query else Card.objects.all()

    paginator = Paginator(cards, 20)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    prev_url = f'?page={page.previous_page_number()}' if page.has_previous() else ''
    next_url = f'?page={page.next_page_number()}' if page.has_next() else ''

    context = {
        'page_object': page,
        'form': form,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request,
                  'cards/main_page_content.html',
                  context=context
                  )


def card_detail(request, card_number):
    card = Card.objects.get(card_number__iexact=card_number)
    products_on_check = [
        'Мобильный телефон Samsung Galaxy M32',
        'Мобильный телефон Samsung Galaxy M52 5G',
        'Мобильный телефон Samsung Galaxy A53 5G',
        'Мобильный телефон Samsung Galaxy A32',
        'Мобильный телефон Xiaomi Redmi Note 11'
    ]
    if Check.objects.filter(card_id=card):
        checks = Check.objects.filter(card_id=card)
        products = Product.objects.filter(check_id__card_id=card)
    else:
        objs_checks = [
            Check(
                identifier=random.randint(100, 1000000),
                card_id=random.choice(list(Card.objects.all()))
            )
            for _ in range(random.randint(1, 5))
        ]
        checks = Check.objects.bulk_create(objs_checks)

        objs_prod = [
            Product(
                name=random.choice(products_on_check),
                cost=random.randint(1, 1000),
                check_id=random.choice(list(Check.objects.all()))
            )
            for _ in range(random.randint(2, 10))
        ]
        products = Product.objects.bulk_create(objs_prod)

    if request.method == 'POST' and 'save' in request.POST:
        if card.card_status == request.POST['status']:
            message = 'Змін немає'
        else:
            Card.objects.filter(card_number=card_number, card_status=card.card_status)\
                .update(card_status=request.POST['status'])
            card = Card.objects.get(card_number__iexact=card_number)
            message = 'Зміни збережено'
        messages.info(request, message)

    elif request.method == 'POST' and 'delete' in request.POST:
        card.delete()
        message = 'Запис видалено'
        messages.info(request, message=message)
        return redirect('cars_list_url')

    for check in checks:
        cost = 0
        for product in Product.objects.filter(check_id=check):
            cost += product.cost
        Check.objects.filter(identifier=check.identifier).update(total_cost=cost)

    return render(
        request,
        'cards/card_detail.html',
        context={
            'card': card,
            'checks': checks,
            'products': products
        })
