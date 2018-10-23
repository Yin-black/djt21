class FormMixin:
    def get_error(self,form):
        """
        获取form表单错误信息
        :return:
        """
        if hasattr(form,'errors'):
            erro_list = form.errors.get_json_data()
            erro_dict = erro_list.popitem()[1][0]
            # print(erro_list['message'])
            return erro_dict['message']
        return None