from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

# Create your views here.
class ContactView(View):
    def get(self, request):
        return render(request, 'course/contactus.html')