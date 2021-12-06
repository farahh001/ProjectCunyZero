from django.urls import path
from . import views

app_name="course"

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('contact/', views.ContactView.as_view(), name="ContactView"),
    path('about-us/', views.AboutView.as_view(), name="AboutView"),
    path('admin-area/', views.AdminAreaView.as_view(), name="AdminAreaView"),
    # path('admin-complain/', views.AdminComplainView.as_view(), name="AdminComplainView"),
    # path('admin-warning/', views.AdminWarningView.as_view(), name="AdminWarningView"),
    path('student-area/', views.StudentAreaView.as_view(), name="StudentAreaView"),
    path('instructor-area/', views.InstructorAreaView.as_view(), name="InstructorAreaView"),
    # path('manage-complain/', views.ManageComplainView.as_view(), name="ManageComplainView"),
    # path('manage-warning/', views.ManageWarningView.as_view(), name="ManageWarningView"),
]
