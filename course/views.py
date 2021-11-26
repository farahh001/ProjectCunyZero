from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View
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
        return render(request, 'course/admin-area.html')
