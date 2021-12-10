from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import View
from accounts.models import Application, Grade, Profile
from course.forms import ClassForm, SemesterForm
from course.models import Class, ClassRequest, Complain, Review, Semester, ShoppingCart, TabooWord, Warning
import datetime
from course.utils import time_to_timestamp

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

class CreateSemesterView(View):
    def post(self, request):

        start_date = request.POST.get('start_date', '').split('-')
        start_date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])).date()

        end_date = request.POST.get('end_date', '').split('-')
        end_date = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2])).date()

        setup_period_date = request.POST['setup_period_date']
        setup_period_time = request.POST['setup_period_time']

        setup_period_date = request.POST.get('setup_period_date', '').split('-')
        setup_period_time = request.POST.get('setup_period_time', '').split(':')

        setup_period = datetime.datetime(
                                int(setup_period_date[0]),
                                int(setup_period_date[1]),
                                int(setup_period_date[2]),
                                int(setup_period_time[0]),
                                int(setup_period_time[1])
                            )

        registration_period_date = request.POST['registration_period_date']
        registration_period_time = request.POST['registration_period_time']

        registration_period_date = request.POST.get('registration_period_date', '').split('-')
        registration_period_time = request.POST.get('registration_period_time', '').split(':')

        registration_period = datetime.datetime(
                                int(registration_period_date[0]),
                                int(registration_period_date[1]),
                                int(registration_period_date[2]),
                                int(registration_period_time[0]),
                                int(registration_period_time[1])
                            )

        running_period_date = request.POST['running_period_date']
        running_period_time = request.POST['running_period_time']

        running_period_date = request.POST.get('running_period_date', '').split('-')
        running_period_time = request.POST.get('running_period_time', '').split(':')

        running_period = datetime.datetime(
                                int(running_period_date[0]),
                                int(running_period_date[1]),
                                int(running_period_date[2]),
                                int(running_period_time[0]),
                                int(running_period_time[1])
                            )

        grading_period_date = request.POST['grading_period_date']
        grading_period_time = request.POST['grading_period_time']

        grading_period_date = request.POST.get('grading_period_date', '').split('-')
        grading_period_time = request.POST.get('grading_period_time', '').split(':')

        grading_period = datetime.datetime(
                                int(grading_period_date[0]),
                                int(grading_period_date[1]),
                                int(grading_period_date[2]),
                                int(grading_period_time[0]),
                                int(grading_period_time[1])
                            )

        semester = Semester(
            start_date = start_date,
            end_date = end_date,
            setup_period = setup_period,
            registration_period = registration_period,
            running_period = running_period,
            grading_period = grading_period,
        )

        try:
            semester.clean()
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse("course:AdminAreaView"))

        semester.save()
        messages.success(request, "Semester Created Successfully.")
        return HttpResponseRedirect(reverse("course:AdminAreaView"))


class DeavtivateSemesterView(View):
    def post(self, request):
        print(request.POST)
        semester_id = request.POST.get('semester_id', None)
        semester = get_object_or_404(Semester, id = semester_id)
        semester.deactivated = True
        semester.save()
        messages.success(request, "Semester has been deactivated.")
        return HttpResponseRedirect(reverse("course:AdminAreaView"))

class CreateClassView(View):
    def post(self, request):

        semester_id = request.POST.get('semester_id', '')
        semester = get_object_or_404(Semester, id = semester_id)

        instructor = request.POST.get('instructor', '')
        instructor = get_object_or_404(Profile, id = instructor)

        start_date = request.POST.get('start_date', '').split('-')
        start_date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])).date()

        end_date = request.POST.get('end_date', '').split('-')
        end_date = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2])).date()

        start_time = request.POST.get('start_time', '').split(':')
        start_time = datetime.time(int(start_time[0]), int(start_time[1]))

        end_time = request.POST.get('end_time', '').split(':')
        end_time = datetime.time(int(end_time[0]), int(end_time[1]))

        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        instructions = request.POST.get('instructions', '')
        quota = request.POST.get('quota', '')

        _class = Class(
            semester = semester,
            title = title,
            description = description,
            instructions = instructions,
            quota = quota,
            instructor = instructor,
            start_date = start_date,
            end_date = end_date,
            start_time = start_time,
            end_time = end_time,
        )
        _class.save()

        messages.success(request, "Class has been created Successfully.")
        return HttpResponseRedirect(reverse("course:AdminAreaView"))




class ManageGradeView(View):
    def post(self, request):
        rating = request.POST.get('rating', None)
        student_id = request.POST.get('student_id', None)
        class_id = request.POST.get('class_id', None)
        instructor_id = request.POST.get('instructor_id', None)
        _class = get_object_or_404(Class, id=class_id)
        student = get_object_or_404(Profile, id=student_id)
        instructor = get_object_or_404(Profile, id=instructor_id)

        print(float(rating))

        Grade.objects.create(
            GPA = float(rating),
            by_instructor = instructor,
            to_student = student,
            refferring_class = _class,
        )

        messages.success(request, "Grade Given Successfully")

        return redirect(f"{reverse('course:InstructorCourseDetailView')}?id={_class.id}")


class InstructorCourseDetailView(View):
    def get(self, request):
        class_id = request.GET.get("id", None)
        _class = get_object_or_404(Class, id=class_id)
        context = {"class": _class}
        return render(request, "course/student-grading.html", context)


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

class EnrollRequestView(View):
    def get(self, request):
        if not request.user.profile.role == "ins":
            return HttpResponseRedirect(reverse("course:HomeView"))
        return render(request, "course/enroll-requests.html")

    def post(self, request):
        request_id = request.POST.get('request_id', None)
        action = request.POST.get('action', None)
        request_instance = get_object_or_404(ClassRequest, id=request_id)

        if action == "reject":
            request_instance.delete()
            messages.success(request, "Request Deleted")
        elif action == "accept":
            class_instance = request_instance.course
            profile = request_instance.user
            cart, created = ShoppingCart.objects.get_or_create(user=profile)

            if not class_instance.quota <= len(class_instance.enrolled_by.all()):
                if not len(profile.get_current_classes) >= 4:
                    conflict = False
                    for enrolled_class in profile.get_current_classes:
                        start_time = time_to_timestamp(enrolled_class.start_time)
                        end_time = time_to_timestamp(enrolled_class.end_time)
                        new_start_time = time_to_timestamp(class_instance.start_time)
                        new_end_time = time_to_timestamp(class_instance.end_time)
                        if (start_time < new_end_time and new_start_time < end_time):
                            conflict = True
                    if not conflict:
                        class_instance.enrolled_by.add(profile)
                        class_instance.save()
                        messages.success(request, "Request Accepted")
                        cart.courses.remove(class_instance)
                    else:
                        messages.error(request, "There's a time conflict between classes of Student.")
                else:
                    messages.error(request, "Max Class Enroll Limit Reached By Student")
            else:
                messages.error(request, "Your Class is full.")

        return HttpResponseRedirect(reverse("course:StudentCartView"))

class CourseDetailView(View):
    def get(self, request):
        class_id = request.GET.get("id", None)
        _class = get_object_or_404(Class, id=class_id)
        context = {"class": _class}
        return render(request, "course/course-detail.html", context)

class ReceivedWarningsView(View):
    def get(self, request):

        return render(request, 'course/received-warnings.html')




class ManageReviewView(View):
    def post(self, request):
        review_id = request.POST.get('review_id', None)
        comment_body = request.POST.get('comment_body', '')
        stars = request.POST.get('stars', None)
        _class_id = request.POST.get('class_id', None)
        action = request.POST.get('action', None)
        _class = get_object_or_404(Class, id=_class_id)

        taboo_words = TabooWord.objects.all().values_list("word")

        word_occurrence = 0
        for word in taboo_words:
            if word[0] in comment_body:
                comment_body = comment_body.replace(word[0], "***")
                word_occurrence += 1
        
        if word_occurrence >= 1:
            user = request.user

            semesters = Semester.objects.filter(deactivated=False)
            active_semester = [semester for semester in semesters if semester.is_active]
            if active_semester:
                active_semester = active_semester[0]
            else:
                active_semester = None

            Warning.objects.create(
                profile = user.profile,
                message = f"There were ({word_occurrence}) Taboo Words in your review.",
                reason = "Using Taboo words in review.",
                semester = active_semester,
            )
            if word_occurrence >= 3:
                Warning.objects.create(
                    profile = user.profile,
                    message = f"There were ({word_occurrence}) Taboo Words in your review.",
                    reason = "Using Taboo words in review.",
                    semester = active_semester,
                )
                messages.warning(request, f"({word_occurrence}) Taboo words were detected in your review and you have recieved (2) warning.")
            else:
                messages.warning(request, f"({word_occurrence}) Taboo words were detected in your review and you have recieved (1) warning.")



        if action == "add":
            Review.objects.create(
                by_profile = request.user.profile,
                refferring_class = _class,
                body = comment_body,
                stars = int(stars),
            )
        elif action == "delete":
            review = get_object_or_404(Review, id=review_id)
            if review.by_profile == request.user.profile:
                review.delete()
            else:
                return HttpResponseForbidden()
        return redirect(f"{reverse('course:CourseDetailView')}?id={_class.id}")

class ManageGradeView(View):
    def post(self, request):
        rating = request.POST.get('rating', None)
        student_id = request.POST.get('student_id', None)
        class_id = request.POST.get('class_id', None)
        instructor_id = request.POST.get('instructor_id', None)
        _class = get_object_or_404(Class, id=class_id)
        student = get_object_or_404(Profile, id=student_id)
        instructor = get_object_or_404(Profile, id=instructor_id)

        print(float(rating))

        Grade.objects.create(
            GPA = float(rating),
            by_instructor = instructor,
            to_student = student,
            refferring_class = _class,
        )

        messages.success(request, "Grade Given Successfully")

        return redirect(f"{reverse('course:InstructorCourseDetailView')}?id={_class.id}")


class StudentCartView(View):
    def get(self, request):
        if not request.user.profile.role == "std":
            return HttpResponseRedirect(reverse("course:HomeView"))
        query = request.GET.get("q", None)
        search_results = None
        if query:
            search_results = Class.objects.filter(Q(title__contains = query) | Q(description__contains = query))
        cart = request.user.profile.carts.all().first()
        context = {"cart": cart, "search_results": search_results, "query": query}
        return render(request, "course/classes.html", context)

    def post(self, request):
        class_id = request.POST.get('class_id', None)
        action = request.POST.get('action', None)
        class_instance = get_object_or_404(Class, id=class_id)
        cart, created = ShoppingCart.objects.get_or_create(user=request.user.profile)
        if action == "delete":
            cart.courses.remove(class_instance)
            messages.success(request, "Class Dropped")
        elif action == "enroll":
            if not class_instance.quota <= len(class_instance.enrolled_by.all()):
                if not len(request.user.profile.get_current_classes) >= 4:
                    conflict = False
                    for enrolled_class in request.user.profile.get_current_classes:
                        start_time = time_to_timestamp(enrolled_class.start_time)
                        end_time = time_to_timestamp(enrolled_class.end_time)
                        new_start_time = time_to_timestamp(class_instance.start_time)
                        new_end_time = time_to_timestamp(class_instance.end_time)
                        if (start_time < new_end_time and new_start_time < end_time):
                            conflict = True
                    if not conflict:
                        if request.user.profile.get_gpa >= 3:
                            class_instance.enrolled_by.add(request.user.profile)
                            class_instance.save()
                            messages.success(request, "Class Enrolled")
                            cart.courses.remove(class_instance)
                        else:
                            semesters = Semester.objects.filter(deactivated=False)
                            active_semester = [semester for semester in semesters if semester.is_active]
                            if active_semester:
                                active_semester = active_semester[0]
                            else:
                                active_semester = None
                                
                            enroll_request, created = ClassRequest.objects.get_or_create(
                                user = request.user.profile,
                                semester = active_semester,
                                course = class_instance
                            )
                            if not created:
                                messages.info(request, "Your request has already been sent to the instructor.")
                            else:
                                messages.success(request, "Your request has been sent to the instructor.")
                    else:
                        messages.error(request, "There's a time conflict between classes.")
                else:
                    messages.error(request, "Max Class Enroll Limit Reached")
            else:
                messages.error(request, "Class is full.")
            
        return HttpResponseRedirect(reverse("course:StudentCartView"))
    