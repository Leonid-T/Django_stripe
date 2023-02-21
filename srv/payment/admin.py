from django.contrib import admin

from .models import Item, Order, OrderItem, Discount, Currency


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
admin.site.register(Currency)
