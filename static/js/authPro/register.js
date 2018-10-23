$(function () {
    var graphcaptchaBtn = $('.form-item .captcha-graph-img');
    var graphcaptchaImg =graphcaptchaBtn.find('img');
    
    //刷新随机图片
    graphcaptchaBtn.click(function () {
        var oldSrc = graphcaptchaImg.attr('src');
        var newSrc = oldSrc.split("?")[0] + "?_" + Date.now();
        graphcaptchaImg.attr('src',newSrc);
        // console.log(oldSrc)
        //给图片增加时间戳，以用来更新随机图片
    });
    
    // 发送验证码
    var sendsmsBtn = $('.form-item .sms-captcha');

    sendsmsBtn.click(function () {
        var telVal = $("input[name='telephone']").val();  //手机号

        let reg=/^1[3-9][0-9][0-9]{8}$/;

        if(telVal && telVal.trim()){
            if(reg.test((telVal))) {
                $.ajax({
                    url: "/auth/send_sms/",
                    method: 'get',
                    dataType: 'json',
                    data: {
                        'telephone': telVal,
                    },
                    success: res => {
                        console.log(res);

                        // var res_obj = JSON.parse(res);
                        // console.log(res_obj);
                        // if (res_obj['Code'] === 'OK') {
                        //     message.showSuccess('验证码发送成功！');
                        //     var count =60;
                        //     var text = $(this).text();
                        //     $(this).attr('disabled',true);
                        //
                        //     var timer = setInterval(()=> {
                        //         $(this).text(count);
                        //         count--;
                        //         if(count<0){
                        //             clearInterval(timer);
                        //             $(this).text('发送验证码')
                        //             $(this).attr('disabled',false);
                        //         }
                        //     },1000);
                        // }
                        // else{
                        //     message.showError('验证码发送失败！')
                        // }
                    },
                    error: res => {

                    },
                })
            }
            else{
                message.showError("手机号格式不对")
                 $("input[name='telephone']").focus()
            }
        }
        else{
            message.showError("手机号不能为空！");
             $("input[name='telephone']").focus()
        }
    })


    //提交注册
    var regBtn = $(".form-item .register-btn");

    regBtn.click(()=> {
        var telephone = $("input[name='telephone']").val();
        var sms_captcha = $('input[name="sms_captcha"]').val().toLowerCase();
        var username = $('input[name="username"]').val();
        var password = $('input[name="password"]').val();
        var password_repeat = $('input[name="password_repeat"]').val();
        var captcha_graph = $('input[name="captcha_graph"]').val().toLowerCase();

        if(username && username.trim() && password && password.trim()){
            if(password === password_repeat){
                 $.ajax({
                     url:"/auth/register/",
                     method:'post',
                     dataType:"json",
                     data:{
                         'telephone':telephone,
                         'sms_captcha':sms_captcha,
                         'username':username,
                         'password':password,
                         'password_repeat':password_repeat,
                         'captcha_graph':captcha_graph,
                     },
                     success:res=>{
                         if(res['code'] === 2){
                            message.showSuccess(res['msg']);
                            setTimeout(()=>{
                                window.location.href='/';  //延时2秒跳转到登陆页面
                            },2000)
                         }
                         else{
                             message.showError(res['msg']);

                         }
                     },
                     error:res=>{},
                 })
            }
            else{
                message.showError("两次密码不正确")
            }
        }
        else{
            message.showError("用户名或密码不能为空！")
        }
    })
    
});