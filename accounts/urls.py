from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('logout/', views.LogOutView.as_view(), name="LogOutView"),
    path('login/', views.LogInView.as_view(), name="LogInView"),
    path('signup/', views.HandleSignUp.as_view(), name="HandleSignUp"),
    path('apply/', views.ApplyView.as_view(), name="ApplyView"),
    path('manage-application/', views.ManageApplicationView.as_view(), name="ManageApplicationView"),
    path('manage-uuid/', views.SignUpWithUUID.as_view(), name="SignUpWithUUID"),
    path('new-signup/', views.SignUpView.as_view(), name="SignUpView"),
    path('download/', views.DownloadFileView.as_view(), name="DownloadFileView"),
]
# 6333fbdc-4dbe-11ec-96da-3b9900e494a4
