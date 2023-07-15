from .views import OrderList, Identify
from django.urls import path

urlpatterns = [
    path('', OrderList.as_view()),
    path('identify', Identify.as_view()),
]