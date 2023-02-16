from django.urls import path

from . import views


app_name = 'payment'
urlpatterns = [
    path('buy/<int:pk>', views.CreateCheckoutSessionView.as_view(), name='buy'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='detail'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]