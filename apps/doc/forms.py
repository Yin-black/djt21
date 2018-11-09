from django import  forms
from .models import Doc

class DocUploadForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = '__all__'
        error_messages = {
            "file_path": {
                "required": "文件路径不能为空"
            },
            "title": {
                "required": "文档标题不能为空"
            }
        }