from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View
from course.models import Class


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'course/home.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'course/contactus.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'course/about_us.html')

class AdminAreaView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("course:HomeView"))
        
        pending_students = Application.objects.filter(role="std", approved=False, rejected=False)
        pending_instructors = Application.objects.filter(role="ins", approved=False, rejected=False)
        class_form = ClassForm(request.POST)
        # semester_form = SemesterForm()
        context = {"pending_instructors": pending_instructors, "pending_students": pending_students, "class_form": class_form}

class StudentAreaView(View):
    def get(self, request):
        profile = request.user.profile
        if not profile.role == "std":
            return HttpResponseRedirect(reverse("course:HomeView"))
        enrolled_class_ids = [_class.id for _class in profile.get_current_classes]
        available_classes = Class.objects.filter(~Q(id__in=enrolled_class_ids))
        available_classes = [_class for _class in available_classes if _class.is_active]
        context = {"available_classes": available_classes}
        return render(request, 'course/student-area.html', context)