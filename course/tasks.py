from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from django.db.models.aggregates import Count


def handle_semester_stage():
    from accounts.models import Profile
    from course.models import Class, Semester, Warning, LabelOfHonor

    semesters = Semester.objects.filter(deactivated=False)
    active_semester = [semester for semester in semesters if semester.is_active]
    if active_semester:
        active_semester = active_semester[0]
    
    status = active_semester.get_status
    
    if status == "Setup":
        print("Setup")
        pass
    elif status == "Registration":
        print("Registration")
        pass
    elif status == "Running":
        print("Running")
        classes = active_semester.classes.all()
        classes_to_cancel = classes.annotate(num_students=Count('enrolled_by')).filter(num_students__lte=5)
        
        for _class in classes_to_cancel:
            _class.cancelled = True
            _class.save()
            
        students = Profile.objects.filter(role="std")
        for student in students:
            classess = student.get_current_classes
            if len(classess) < 2:
                Warning.objects.create(
                    profile = student,
                    message = "You didn't enroll enough courses.",
                    reason = "less than 2 courses enrolled",
                    semester = active_semester,
                )
    elif status == "Grading":
        print("Grading")
        pass
    elif status == "Grading_Ended":
        print("Grading_Ended")
        students = Profile.objects.filter(role="std")
        students = [student for student in students if student.get_gpa < 2]
        for student in students:
            student.suspended = True
            student.save()

        students = [student for student in students if student.get_gpa >= 2 and student.get_gpa <= 2.25]
        for student in students:
            Warning.objects.create(
                profile = student,
                message = f"Your GPA is ({student.get_gpa}).",
                reason = "GPA is between 2-2.25",
                semester = active_semester,
            )
            student.save()

        students = [student for student in students if student.get_gpa >= 3.5]
        for student in students:
            LabelOfHonor.objects.get_or_create(
                semester = active_semester,
                user = student,
            )
    return True



# @periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
# def some_task():
#     # do something
