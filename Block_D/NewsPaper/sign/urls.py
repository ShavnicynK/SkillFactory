from django.urls import path
from .models import AccountView
from .views import set_author

urlpatterns = [
    path('account/', AccountView.as_view(), name="account_view"),
    path('upgrade/', set_author, name='upgrade'),
]