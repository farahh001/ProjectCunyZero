from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('logout/', views.LogOutView.as_view(), name="LogOutView"),
    path('login/', views.LogInView.as_view(), name="LogInView"),
    path('signup/', views.SignUpView.as_view(), name="SignUpView"),

]
