$(function () {

    // 登陆按钮
    $(".login-btn").click(function () {
        var telVal = $("input[name='telephone']").val();
        var pwdVal = $("input[name='password']").val();
        var $remember = $("input[name='remember']")
        // console.log(pwdVal);
        var checkVal = $remember.is(":checked")
        if(pwdVal && telVal){
            var data={
                    'telephone': telVal,
                    'password' : pwdVal,
                }
            if (checkVal){
                data['remember'] = checkVal ;
            }
            // console.log(checkVal)
            $.ajax({
                url:'/auth/login/',
                method:'post',
                dataType:'json',
                success: error=> {
                    // console.log(error)
                    if(error['code'] == 1) {   //错误
                        swal({title: error['msg'],type:"error",timer:2000,
  showConfirmButton:false});
                        }
                    else if(error['code'] == 2)   //登陆成功
                    {

                        message.showSuccess(error['msg']);
                        setTimeout(()=>{
                           window.location.href='/';
                        },2000)
                         //延时2秒跳转到主页
                    }
                },
                data:data,
                error: eror=> {
                    console.log(eror)

                }
            });
        }
        else
        {
            message.showError("手机号和密码不能为空！");}
    })
});