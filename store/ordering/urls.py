from django.urls import path
from .views import OrderViewStep1, OrderViewStep2, OrderViewStep3, OrderViewStep4, PaymentOnlineCardView, PaymentSomeoneCardView, OrderDetails


app_name = 'order'

urlpatterns = [
    path('step-1/', OrderViewStep1.as_view(), name='step_1'),
    path('step-2/', OrderViewStep2.as_view(), name='step_2'),
    path('step-3/', OrderViewStep3.as_view(), name='step_3'),
    path('step-4/', OrderViewStep4.as_view(), name='step_4'),
    path('payment-online/', PaymentOnlineCardView.as_view(), name='payment_online'),
    path('payment-someone/', PaymentSomeoneCardView.as_view(), name='payment_someone'),
    path('details/<int:pk>/', OrderDetails.as_view(), name='order_details'),
]