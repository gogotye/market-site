from django.urls import path
from .views import (Login, AuthorLogoutView, RegisterCustomerView, FirstRegisterSellerView, SecondRegisterSellerView,
                    RestorePasswordFirstStep,
                    RestorePasswordSecondStep)


app_name = 'user_app'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),
    path('register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('register/seller/first-step', FirstRegisterSellerView.as_view(), name='register_seller_step_one'),
    path('register/seller/second-step', SecondRegisterSellerView.as_view(), name='register_seller_step_two'),
    path('register/drop-password/first-step/', RestorePasswordFirstStep.as_view(), name='password_first'),
    path('register/drop-password/second-step/', RestorePasswordSecondStep.as_view(), name='password_second'),
]

