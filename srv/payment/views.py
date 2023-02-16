from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views import View, generic
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse

import stripe

from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        domain = request.build_absolute_uri('/')[:-1]
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': item.price,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + reverse('payment:success'),
            cancel_url=domain + reverse('payment:cancel'),
        )
        return JsonResponse({'session_id': session.id}, status=200)


class SuccessView(generic.TemplateView):
    template_name = 'success.html'


class CancelView(generic.TemplateView):
    template_name = 'cancel.html'


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'detail.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Item.objects.filter(pk=pk)
