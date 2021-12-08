from django.urls import path
from . import views

app_name="course"

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('contact/', views.ContactView.as_view(), name="ContactView"),
    path('about-us/', views.AboutView.as_view(), name="AboutView"),
    path('admin-area/', views.AdminAreaView.as_view(), name="AdminAreaView"),
    path('admin-complain/', views.AdminComplainView.as_view(), name="AdminComplainView"),
    path('admin-warning/', views.AdminWarningView.as_view(), name="AdminWarningView"),
    path('student-area/', views.StudentAreaView.as_view(), name="StudentAreaView"),
    path('instructor-area/', views.InstructorAreaView.as_view(), name="InstructorAreaView"),
    path('manage-complain/', views.ManageComplainView.as_view(), name="ManageComplainView"),
    path('manage-warning/', views.ManageWarningView.as_view(), name="ManageWarningView"),
    path('enroll-requests/', views.EnrollRequestView.as_view(), name="EnrollRequestView"),
    path('class-detail/', views.CourseDetailView.as_view(), name="CourseDetailView"),
    path('create-semester/', views.CreateSemesterView.as_view(), name="CreateSemesterView"),
    path('deactivate-semester/', views.DeavtivateSemesterView.as_view(), name="DeavtivateSemesterView"),
    path('create-class/', views.CreateClassView.as_view(), name="CreateClassView"),
    path('received-warnings/', views.ReceivedWarningsView.as_view(), name="ReceivedWarningsView"),
    path('class-detail-instructor/', views.InstructorCourseDetailView.as_view(), name="InstructorCourseDetailView"),
    path('manage-grade/', views.ManageGradeView.as_view(), name="ManageGradeView"),
     path('manage-review/', views.ManageReviewView.as_view(), name="ManageReviewView"),
]
