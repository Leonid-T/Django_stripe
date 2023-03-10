from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

import stripe


class Currency(models.Model):
    type = models.CharField(max_length=4)
    char = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.type


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.FloatField(validators=[MinValueValidator(0.5)])
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    @property
    def get_price(self):
        """
        Getting price for stripe data
        """
        return int(self.price*100)

    def __str__(self):
        return self.name

    def get_price_data(self):
        """
        Price data for line_items in stripe.checkout.Session
        """
        price_data = {
            'currency': self.currency.type,
            'unit_amount': self.get_price,
            'product_data': {
                'name': self.name,
                'description': self.description,
            },
        }
        return price_data


class Discount(models.Model):
    percent_off = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.percent_off} %'


class Order(models.Model):
    customer = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Order of {self.customer}'

    def total_price(self):
        """
        Total price with discount
        """
        coupon = self.discount.percent_off/100 if self.discount else 0
        return round(sum(item.total_price() for item in self.items.all()) * (1 - coupon), 2)

    def get_line_items(self):
        """
        Create line_items for stripe.checkout.Session
        """
        return [item.get_buy_data() for item in self.items.all()]

    def get_discounts(self):
        """
        Create discounts for stripe.checkout.Session
        """
        if self.discount:
            return [{'coupon': stripe.Coupon.create(percent_off=self.discount.percent_off)}]
        return []


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        """
        Validation of equal item's currency in order
        """
        if self.item.currency != self.order.currency:
            raise ValidationError('Currency of items should not be different')

    def total_price(self):
        """
        Total price of one item of goods
        """
        return round(self.item.price * self.quantity, 2)

    def get_buy_data(self):
        """
        Create item for line_items in stripe.checkout.Session
        """
        buy_data = {
            'price_data': self.item.get_price_data(),
            'quantity': self.quantity,
        }
        return buy_data
