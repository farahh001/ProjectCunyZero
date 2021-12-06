from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
import uuid
import mimetypes
import os
from django.conf import settings
from .models import Application, UserUniqueId
from .forms import SignUpForm



# Create your views here.

class HandleSignUp(View):
    def get(self, request):
        _uuid = request.session.get("user_uuid", None)
        try:
            user_uuid_instance = UserUniqueId.objects.get(uuid = _uuid, expired = False)
        except:
            user_uuid_instance = None
        
        if _uuid and user_uuid_instance:
            form = SignUpForm()
            context = {'form': form}
            messages.success(request, "Please Continue Your SignUp.")
            return render(request, 'accounts/signup.html', context)
        else:
            return render(request, 'accounts/uuid_signup.html')

class SignUpWithUUID(View):

    def post(self, request):
        _uuid = request.POST.get('uuid', None)
        if _uuid:
            # form.save()
            user_uuid_instance = get_object_or_404(UserUniqueId, uuid = _uuid)
            # user_uuid_instance.expired = True
            # user_uuid_instance.save()
            request.session["user_uuid"] = user_uuid_instance.uuid
            return HttpResponseRedirect(reverse("accounts:HandleSignUp"))
        raise Http404()



class SignUpView(View):
    # def get(self, request):
    #     form = SignUpForm()
    #     context = {'form': form}
    #     return render(request, 'accounts/signup.html', context)

    def post(self, request):
        _uuid = request.session.get("user_uuid", None)

        try:
            user_uuid_instance = UserUniqueId.objects.get(uuid = _uuid, expired = False)
        except:
            user_uuid_instance = None

        if not _uuid or not user_uuid_instance:
            raise ValidationError("UUID is incorrect")

        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()

            user.first_name = user_uuid_instance.application.first_name
            user.last_name = user_uuid_instance.application.last_name
            user.profile.image = form.cleaned_data.get('image')
            user.profile.role = user_uuid_instance.application.role

            user.profile.save()
            user.save()

            user_uuid_instance.user = user
            user_uuid_instance.expired = True
            user_uuid_instance.save()

            request.session.flush()

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

