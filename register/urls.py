from django.urls import path 
from register import views 

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]