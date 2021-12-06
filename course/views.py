from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import View
from accounts.models import Application, Grade, Profile
#from course.forms import ClassForm, SemesterForm
from course.models import Class
import datetime
#from course.utils import time_to_timestamp

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


class InstructorAreaView(View):
    def get(self, request):
        profile = request.user.profile
        if not profile.role == "ins":
            return HttpResponseRedirect(reverse("course:HomeView"))
        return render(request, 'course/instructor-area.html')

class ManageClassView(View):
    def post(self, request):
        if not request.user.profile.role == "std":
            return HttpResponseRedirect(reverse("course:HomeView"))
        class_id = request.POST.get('class_id', None)
        action = request.POST.get('action', None)
        class_instance = get_object_or_404(Class, id=class_id)
        if action == "drop":
            class_instance.enrolled_by.remove(request.user.profile)
            messages.success(request, "Class Dropped")
        elif action == "enroll":
            """Add's class to cart. Enroll is at StudentCartView"""
            cart, created = ShoppingCart.objects.get_or_create(user=request.user.profile)
            cart.courses.add(class_instance)
            messages.success(request, "Class added to the cart.")
            
            # if not class_instance.quota <= len(class_instance.enrolled_by.all()):
            #     if not len(request.user.profile.get_current_classes) >= 4:
            #         conflict = False
            #         for enrolled_class in request.user.profile.get_current_classes:
            #             start_time = time_to_timestamp(enrolled_class.start_time)
            #             end_time = time_to_timestamp(enrolled_class.end_time)
            #             new_start_time = time_to_timestamp(class_instance.start_time)
            #             new_end_time = time_to_timestamp(class_instance.end_time)
            #             if (start_time < new_end_time and new_start_time < end_time):
            #                 conflict = True
            #         if not conflict:
            #             class_instance.enrolled_by.add(request.user.profile)
            #             class_instance.save()
            #             messages.success(request, "Class Enrolled")
            #         else:
            #             messages.error(request, "There's a time conflict between classes.")
            #     else:
            #         messages.error(request, "Max Class Enroll Limit Reached")
            # else:
            #     messages.error(request, "Class is full.")
        return HttpResponseRedirect(reverse("course:StudentAreaView"))

class RemoveClassView(View):
    def post(self, request):
        semester_id = request.POST.get('semester_id', None)
        class_id = request.POST.get('class_id', None)
        
        class_instance = get_object_or_404(Class, id=class_id)
        class_instance.delete()
        # semester_instance = get_object_or_404(Semester, id=semester_id)
        # semester_instance.classes.remove(class_instance)
        # semester_instance.save()
        
        messages.success(request, f"Class Removed")
        return HttpResponseRedirect(reverse("course:AdminAreaView")) 

class AdminWarningView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("course:HomeView"))

        students = Profile.objects.filter(role="std")
        instructors = Profile.objects.filter(role="ins")
        recieved_warnings = Warning.objects.filter(deactivated = False)
        
        context = {"recieved_warnings": recieved_warnings, "students": students, "instructors": instructors}
        return render(request, 'course/admin-warnings.html', context)