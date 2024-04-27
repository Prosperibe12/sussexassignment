from django.urls import path 
from webservice import views 

urlpatterns = [
    path('conversion/<str:currency1>/<str:currency2>/<str:amount>/', views.CurrencyConverterAPIView.as_view(), name='currency_convert')
]