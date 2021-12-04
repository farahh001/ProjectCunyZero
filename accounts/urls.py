from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('logout/', views.LogOutView.as_view(), name="LogOutView"),
    path('login/', views.LogInView.as_view(), name="LogInView"),
    path('signup/', views.HandleSignUp.as_view(), name="HandleSignUp"),
    path('signup/', views.SignUpView.as_view(), name="SignUpView"),
    path('apply/', views.ApplyView.as_view(), name="ApplyView"),
    path('manage-application/', views.ManageApplicationView.as_view(), name="ManageApplicationView"),
    path('manage-uuid/', views.SignUpWithUUID.as_view(), name="SignUpWithUUID"),
    path('new-signup/', views.SignUpView.as_view(), name="SignUpView"),
]
