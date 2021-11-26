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
