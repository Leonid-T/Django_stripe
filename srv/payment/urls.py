from django.urls import path

from . import views


app_name = 'payment'
urlpatterns = [
    path('buy/<int:pk>', views.CreateCheckoutSessionItemView.as_view(), name='buy'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('order/<int:pk>/buy/', views.CreateCheckoutSessionOrderView.as_view(), name='buy_order')
]