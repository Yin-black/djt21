from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from djt21 import settings
from apps.doc.models import Doc
from apps.doc.forms import DocUploadForm
from apps.authPro.formcheck import FormMixin
from utils import json_status
import os
from django.contrib.admin.views.decorators import staff_member_required

@method_decorator([csrf_exempt, ], name="dispatch")
class DocUploadView(View,FormMixin):

    def get(self, request):
        return render(request, 'cms/doc/doc_upload.html')

    def post(self, request):
        form = DocUploadForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            file_path = form.cleaned_data.get("file_path")
            Doc.objects.create(title=title, desc=desc, file_path=file_path, auth=request.user)
            return json_status.result(message='文档保存成功！')
        # print(form.errors)
        return json_status.params_error(message=self.get_error(form))

@method_decorator([csrf_exempt, staff_member_required(login_url='/auth/login/')], name='dispatch')
class UploadFileView(View):
    """
    上传到服务器
    """

    def post(self, request):
        filepath = settings.DOC_ROOT
        f = request.FILES.get('upload_file')
        filename = os.path.join(filepath, f.name).encode('utf-8')

        with open(filename, 'wb') as file:
            for chunk in f.chunks():
                file.write(chunk)
        fileurl = request.build_absolute_uri(settings.DOC_URL + f.name)  # 生成一个可访问的url地址

        return json_status.result(message="sucess", data={"file_url": fileurl})