from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views import View, generic
from django.urls import reverse
from django.http import JsonResponse

import stripe

from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionItemView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        domain = request.build_absolute_uri('/')[:-1]
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': item.get_price_data(),
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + reverse('payment:success'),
            cancel_url=domain + reverse('payment:cancel'),
        )
        return JsonResponse({
            'session_id': session.id,
            'public_key': settings.STRIPE_PUBLIC_KEY,
        }, status=200)


class CreateCheckoutSessionOrderView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        domain = request.build_absolute_uri('/')[:-1]
        session = stripe.checkout.Session.create(
            line_items=order.get_line_items(),
            discounts=order.get_discounts(),
            mode='payment',
            success_url=domain + reverse('payment:success'),
            cancel_url=domain + reverse('payment:cancel'),
        )
        return JsonResponse({
            'session_id': session.id,
            'public_key': settings.STRIPE_PUBLIC_KEY,
        }, status=200)


class SuccessView(generic.TemplateView):
    template_name = 'success.html'


class CancelView(generic.TemplateView):
    template_name = 'cancel.html'


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'item.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
