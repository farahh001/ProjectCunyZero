from django.urls import path
from . import views

app_name="course"

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('contact/', views.ContactView.as_view(), name="ContactView"),
    path('about-us/', views.AboutView.as_view(), name="AboutView"),
    path('admin-area/', views.AdminAreaView.as_view(), name="AdminAreaView"),
]
