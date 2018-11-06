// 删除按钮的操作
  // 1. 获取按钮
  let $delBtn = $(".btn-del");
  // 2. 触发事件
  $delBtn.click(function () {
    // 2.1 获取绑定在删除按钮上的 新闻 id
    let newsId = $(this).data("news-id");
    swal({
      title: "确定删除新闻吗",
      text: "删除之后，你将无法恢复哦",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "确定删除",
      cancelButtonText: "取消",
      closeOnConfirm: false,
      animation: 'slide-from-top',
    }, () => {
      // 2.2 发起请求
      selfAjax('/cms/news_edit/', 'delete', {"news_id": newsId}, res => {
        if (res["code"] === 2) {
          swal({
            title: "删除",
            type: "success",
          }, () => {
            $(this).parents('tr').remove();
          });
        } else {
          swal({
            title: res["msg"],
            type: "error",
            timer: 1500,
            showCancelButton: false,
            showConfirmButton: false,
          })
        }
      });
    });

  });