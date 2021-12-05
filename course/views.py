from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import View
from accounts.models import Application, Grade, Profile
#from course.forms import ClassForm, SemesterForm
from course.models import Class, Warning, Complain
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

class AdminComplainView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("course:HomeView"))
        
        recieved_complains = Complain.objects.filter(action_taken = False)
        
        context = {"recieved_complains": recieved_complains}
        return render(request, 'course/admin-complains.html', context)


class AdminWarningView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("course:HomeView"))

        students = Profile.objects.filter(role="std")
        instructors = Profile.objects.filter(role="ins")
        recieved_warnings = Warning.objects.filter(deactivated = False)
        
        context = {"recieved_warnings": recieved_warnings, "students": students, "instructors": instructors}
        return render(request, 'course/admin-warnings.html', context)

class ManageComplainView(View):
    def get(self, request):
        # if not request.user.is_staff:
        #     return HttpResponseRedirect(reverse("course:HomeView"))

        students = Profile.objects.filter(role="std")
        instructors = Profile.objects.filter(role="ins")
        context = {"students": students, "instructors": instructors}
        return render(request, 'course/complain.html', context)

    def post(self, request):
        # if not request.user.is_staff:
        #     return HttpResponseRedirect(reverse("course:HomeView"))

        complained_instructor = request.POST.get("complained_instructor", None)
        complained_user = request.POST.get("complained_user", None)
        complain_message = request.POST.get("complain_message", None)
        complain_id = request.POST.get("complain_id", None)
        action = request.POST.get("action", None)
        for_user = None
        print(action)

        if action == "resolved":
            complain = get_object_or_404(Complain, id = complain_id)
            complain.action_taken = True
            complain.save()
            messages.success(request, "Complain resolved successfully")
            return HttpResponseRedirect(reverse("course:AdminComplainView"))
        elif action == "create":
            if complained_instructor and complained_user:
                messages.error(request, "Select only student or instructor at a time!")
                return HttpResponseRedirect(reverse("course:ManageComplainView"))

            if complained_user:
                for_user = get_object_or_404(User, username = complained_user)
            elif complained_instructor:
                for_user = get_object_or_404(User, username = complained_instructor)

            Complain.objects.create(
                message = complain_message,
                by_profile = request.user.profile,
                for_profile = for_user.profile
            )
            messages.success(request, "Complain Submited Successfully")

        return HttpResponseRedirect(reverse("course:HomeView"))
    
class ManageWarningView(View):
    def post(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("course:HomeView"))

        warning_instructor = request.POST.get("warning_instructor", None)
        warning_user = request.POST.get("warning_user", None)
        warning_message = request.POST.get("warning_message", None)
        warning_reason = request.POST.get("warning_reason", None)
        warning_id = request.POST.get("warning_id", None)
        action = request.POST.get("action", None)
        for_user = None
        print(action)

        if action == "delete":
            warning = get_object_or_404(Warning, id = warning_id)
            warning.deactivated = True
            warning.save()
            messages.success(request, "Warning Removed Successfully.")
        if action == "issue":
            if warning_instructor and warning_user:
                messages.error(request, "Select only student or instructor at a time!")
                return HttpResponseRedirect(reverse("course:ManageComplainView"))

            if warning_user:
                for_user = get_object_or_404(User, username = warning_user)
            elif warning_instructor:
                for_user = get_object_or_404(User, username = warning_instructor)

            semesters = Semester.objects.filter(deactivated=False)
            active_semester = [semester for semester in semesters if semester.is_active]
            if active_semester:
                active_semester = active_semester[0]
            else:
                active_semester = None

            Warning.objects.create(
                profile = for_user.profile,
                message = warning_message,
                reason = warning_reason,
                semester = active_semester,
            )

            messages.success(request, "Warning Issued Successfully")

        return HttpResponseRedirect(reverse("course:AdminWarningView"))

