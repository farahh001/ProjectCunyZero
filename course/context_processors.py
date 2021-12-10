from django.utils.translation import deactivate
from accounts.models import Profile
from course.models import Class, Semester
from accounts.models import Application
import operator


def provide_home_info(request):
    students = Profile.objects.filter(role="std")
    for student in students:
        student.GPA = student.get_gpa
        student.save()
    top_students = students.order_by("-GPA")[:10]

    courses = Class.objects.all()
    for course in courses:
        course.rating = course.get_rating
        course.save()
    high_rated_courses = courses.order_by("-rating")[:6]
    low_rated_courses = courses.order_by("rating")[:6]
    
    return dict({"top_students": top_students, "high_rated_courses": high_rated_courses, "low_rated_courses": low_rated_courses})

def provide_active_semester(request):
    semesters = Semester.objects.filter(deactivated=False)
    active_semester = [semester for semester in semesters if semester.is_active]
    if active_semester:
        active_semester = active_semester[0]

    return dict({"active_semester": active_semester})