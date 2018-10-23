from django.shortcuts import render
from django.views import View
# Create your views here.

class Courseview(View):
    def get(self,request):
        return render(request,'course/course.html')