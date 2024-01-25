from django.urls import path
from .views import office, profile, HistoryView, delete_avatar


app_name = 'private_office'

urlpatterns = [
    path('', office, name='office'),
    path('profile/', profile, name='profile'),
    path('history/', HistoryView.as_view(), name='history'),
    path('del-avatar/', delete_avatar, name='del_avatar'),
]