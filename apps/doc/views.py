from django.shortcuts import render
from django.views import View
# Create your views here.

class DocDownloadView(View):
    def get(self,request):
        return render(request,'doc/docDownload.html')