/*
  @author: handsomeFu;
  @Date: 2018/10/16 20:11;
*/
let E = window.wangEditor;
  window.editor = new E('#news-content');
  window.editor.create();
$(function () {

  // 生成富文本编辑器  https://www.kancloud.cn/wangfupeng/wangeditor3/332599


       // editor.txt.html('<p>{{ news_content.content|safe }}</p>')


  // ====================  传文件 ============================
  // 获取缩略图输入框元素
  let $thumbnailUrl = $("#news-thumbnail-url");
  // ================== 上传至七牛（云存储平台） ================
  let $progressBar = $(".progress-bar");
  QINIU.upload({
    // 七牛空间域名
    "domain": "http://pgzhzz0x1.bkt.clouddn.com",
    // 后台返回 token的地址
    "uptoken_url": "/cms/upload_qiniu/",
    // 按钮
    "browse_btn": "upload-btn",
    // 成功
    "success": (up, file, info) => {
      let domain = up.getOption('domain');
      let res = JSON.parse(info);
      let filePath = domain + res.key;
      $thumbnailUrl.val('');
      $thumbnailUrl.val(filePath);
    },
    // 失败
    "error": (up, err, errTip) => {
      console.log('error');
      console.log(up);
      console.log(err);
      console.log(errTip);
      console.log('error');
    },
    // 上传文件的过程中 七牛对于 4M 秒传
    "progress": (up, file) => {
      let percent = file.percent;
      $progressBar.parent().css("display", 'block');
      $progressBar.css("width", percent + '%');
      $progressBar.text(parseInt(percent) + '%');
    },
    // 完成后 去掉进度条
    "complete": () => {
      $progressBar.parent().css("display", 'none');
      $progressBar.css("width", '0%');
      $progressBar.text('0%');
    }
  });
  // ================== 上传至服务器 ================
  let $uploadThumbnail = $("#upload-news-thumbnail");
  $uploadThumbnail.change(function () {
    // 获取文件
    let file = this.files[0];
    // 创建一个 FormData
    let formData = new FormData();
    // 把文件添加进去
    formData.append("upload_file", file);
    // 发送请求
    $.ajax({
      url: "/cms/upload-server/",
      method: "post",
      data: formData,
      // 定义文件的传输
      processData: false,
      contentType: false,
      success: res => {
        console.log(res);
        if (res["code"] === 2) {
          // 获取后台返回的 URL 地址
          let thumbnailUrl = res["data"]["file_url"];
          $thumbnailUrl.val('');
          $thumbnailUrl.val(thumbnailUrl);
        }
      },
      error: err => {
        logError(err);
      }
    });
  });

  // ========= 发表新闻 ==========
  let $newsBtn = $("#btn-pub-news");

  $newsBtn.click(function () {
    let titleVal = $("#news-title").val();
    let descVal = $("#news-desc").val();
    let tagId = $("#news-category").val();
    let thumbnailVal = $thumbnailUrl.val();
    let contentHtml = editor.txt.html();
    let contentText = editor.txt.text();
    //获取绑定在按钮上的news-id属性值
    let news_id= $newsBtn.data('news-id');

    if (tagId === '0') {
      ALERT.alertInfoToast('请选择新闻标签')
    }
    // console.log(`
    //   新闻标题: ${titleVal},
    //   新闻描述: ${descVal},
    //   新闻分类id: ${tagId},
    //   新闻缩略图地址: ${thumbnailVal}
    //   新闻内容html版: ${contentHtml},
    //   新闻内容纯文字版：${contentText}
    // `);
    pu_url = "/cms/pub_news/";
    modi_url ="/cms/news_edit/";
    data =  {
        "title": titleVal,
        "desc": descVal,
        "tag_id": tagId,
        "thumbnail_url": thumbnailVal,
        "content": contentHtml,
      };
    let console_title = '';
    if(news_id){
        data['news_id'] = news_id;
        console_title = '新闻修改成功！'
    }
    else{
        console_title = '新闻发布成功！'
    }

    console.log(news_id);
    console.log(data);
    $.ajax({
      url: news_id?modi_url:pu_url,
      method: "post",
      data:data,
      dataType: "json",
      success: res => {
        // console.log(res);
        if (res["code"] === 2) {
          ALERT.alertNewsSuccessCallback(console_title, '跳到首页', () => {
            window.location.href = '/';
          });
        } else {
          ALERT.alertErrorToast(res["msg"]);
        }
      },
      error: err => {
        logError(err)
      }
    })
  })
});