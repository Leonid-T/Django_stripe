from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_price_data(self):
        price_data = {
            'currency': 'usd',
            'unit_amount': self.price,
            'product_data': {
                'name': self.name,
                'description': self.description,
            },
        }
        return price_data


class Order(models.Model):
    customer = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Order of {self.customer}'

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def get_line_items(self):
        return [item.get_buy_data() for item in self.items.all()]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity

    def get_buy_data(self):
        buy_data = {
            'price_data': self.item.get_price_data(),
            'quantity': self.quantity,
        }
        return buy_data

