import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Doc
from django.http import FileResponse
from utils import json_status
# Create your views here.

@method_decorator([csrf_exempt,], name='dispatch')
class DocDownLoadView(View):
    """文档下载"""
    def get(self,request):

        docs = Doc.objects.filter(is_delete=True)
        return render(request,'doc/docDownload.html',context={'docs':docs})


def doc_download(request):
    # 获取前端传过来的id
    doc_id = request.GET.get("doc_id")
    # 根据id 查出来文档
    doc = Doc.objects.filter(id=doc_id).first()
    if doc:
        # http://192.168.31.200:8000/media/avatar.jpeg
        file_path = doc.file_path
        # requests 返回文件对象
        res = FileResponse(requests.get(file_path))
        # 切出文件后缀
        file_type = file_path.split('.')[-1]
        # 设置文件类型 https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
        if file_type == 'jpg':
            res["Content-type"] = "image/jpeg"
        elif file_type == 'doc':
            res["Content-type"] = "application/msword"
        elif file_type == 'txt':
            res["Content-type"] = "text/plain"
        elif file_type == '.xls':
            res["Content-type"] = 'application/x-xls'
        elif file_type == '.xlsx':
            res["Content-type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            res["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        # 设置附件下载格式
        res["Content-Disposition"] = "attachment; filename={}".format(file_path.split('/')[-1])
        return res
    return json_status.params_error(message="文档不存在")





