from .views import OrderList
from django.urls import path

urlpatterns = [
    path('', OrderList.as_view()),
]