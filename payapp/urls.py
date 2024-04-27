from django.urls import path 
from payapp import views 

urlpatterns = [
    path('dashboard/', views.DashBoard.as_view(), name="dashboard"),
    path('profile/', views.Userprofile.as_view(), name="profile"),
    path('add/',views.AddFunds.as_view(), name="add"),
    path('transfer/', views.TransferFunds.as_view(), name="transfer"),
    path('receive_funds/', views.RequestFunds.as_view(), name="request"),
    path('confirm_payment/<str:id>/', views.ConfirmPaymentRequest.as_view(), name='payment'),
    path('reject_payment/<str:id>/', views.RejectPaymentRequest.as_view(), name='reject_payment')
]