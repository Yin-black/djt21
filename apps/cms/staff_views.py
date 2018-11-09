from django.db.models.query_utils import Q
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import Group
from apps.authPro.models import User
from utils import json_status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from utils.decortors import user_super_required


@method_decorator([csrf_exempt,user_super_required,staff_member_required(login_url='/auth/login/')],name='dispatch')
class StaffView(View):
    """员工展示页面"""

    def get(self,request):
        staffs = User.objects.filter(Q(is_superuser =True)|Q(is_staff = True))
        return render(request,'cms/authPro/staff_view.html',context={'staffs':staffs})

    def post(self,request):
        pass

    def delete(self,request):
        pass

@method_decorator([csrf_exempt,user_super_required,staff_member_required(login_url='/auth/login/')],name='dispatch')
class StaffAddView(View):
    """员工权限添加"""

    def get(self,reqeust):
        groups = Group.objects.all()
        return render(reqeust,'cms/authPro/staff_add.html',context={'groups':groups})

    def post(self,request):

        telephone = request.POST.get('telephone')
        # 获取组列表
        groups = request.POST.getlist('groups')

        if telephone and groups:
            user = User.objects.filter(telephone= telephone).first()

            if user:
                if groups:
                    filter_groups = Group.objects.filter(id__in=groups)
                    user.groups.set(filter_groups)
                    user.is_staff = True
                    user.save()
                    return json_status.result()

            else:
                return json_status.params_error(message='没有这个用户！')
        else:
            return json_status.params_error(message="不能为空！")
