from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


from .models import Application
from .forms import SignUpForm


# Create your views here.



class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()
            user.profile.image = form.cleaned_data.get('image')
            user.profile.save()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("course:HomeView"))
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Successfully Logged Out.")
        return HttpResponseRedirect(reverse('course:HomeView'))


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return HttpResponseRedirect(reverse('course:HomeView'))
        form = AuthenticationForm()
        context = {'form' : form}
        return render(request,'accounts/login.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('course:HomeView'))
        else:
            form = AuthenticationForm(request.POST)
            context = {'form' : form}
            return render(request,'accounts/login.html', context)


class ApplyView(View):
    def get(self, request):
        return render(request, 'accounts/apply.html')

    def post(self, request):
        document = request.FILES.get('document', None)
        role = request.POST.get('role', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        
        if document and role:
            Application.objects.create(
                first_name = first_name,
                last_name = last_name,
                document = document,
                role = role,
            )
            messages.success(request, "Application has been submited successfully.")
            return HttpResponseRedirect(reverse("course:HomeView"))
        messages.error(request, "Application form is not correct.")
        return render(request, 'accounts/apply.html')
    
class ManageApplicationView(View):

    def post(self, request):
        action = request.POST.get('action', None)
        application_id = request.POST.get('application_id', None)
        application = get_object_or_404(Application, id=application_id)
        print(action)
        if action == "approve":
            application.approved = True
            application.rejected = False
        elif action == "reject":
            application.approved = False
            application.rejected = True
        application.save()

        messages.success(request, f"Application has been {action}")
        return HttpResponseRedirect(reverse("course:AdminAreaView"))

