from accounts.models import Profile
from course.models import Course
from accounts.models import Application


def provide_home_info(request):
    top_students = Profile.objects.all()[:6]
    high_rated_courses = Course.objects.all()[:6]
    low_rated_courses = Course.objects.all()[:6]
    
    return dict({"top_students": top_students, "high_rated_courses": high_rated_courses, "low_rated_courses": low_rated_courses})

def provide_pending_approve(request):
    pending_students = Application.objects.filter(role="std", approved=False, rejected=False)
    pending_instructors = Application.objects.filter(role="ins", approved=False, rejected=False)
    
    return dict({"pending_instructors": pending_instructors, "pending_students": pending_students})