// let videoUrl = "http://ik1num9y16fzv5panx1.exp.bcevod.com/mda-ik5iju01rnifvhfi/mda-ik5iju01rnifvhfi.m3u8";
// let videoThumbnail = "http://ik1num9y16fzv5panx1.exp.bcevod.com/mda-ik5iju01rnifvhfi/mda-ik5iju01rnifvhfi.jpg";
  let videoUrl = $("#course-video span").data('video-url');
  let videoThumbnail = $("#course-video span").data('covel-url')
  let player = cyberplayer("course-video").setup({
    width: '100%', // 高度
    height: 650, // 宽度
    file: videoUrl, // 地址
    image: videoThumbnail, //预览图
    autostart: false, // 自动播放
    stretching: "exactfit", // 缩放方式，缩放方式分为：1.none:不缩放；2.uniform:添加黑边缩放；3. exactfit:改变宽高比缩到最大；4.fill:剪切并缩放到最大（默认方式为uniform）
    repeat: false, // 重复播放
    volume: 77, // 音量
    controls: 'over', // 控制条显示
    tokenEncrypt: true,
    ak: '0babce9053614d1488a3c234e690be76', // AccessKey
  });
  player.on('beforePlay', (e) => {
    // 判断文件是否加密
    if(!/m3u8/.test(e.file)){
      return false;
    }
    $.get({
      "url": "/course/course-token/",
      "data": {
        "video_url": videoUrl,
      },
      "success": res => {
        let token = res['token'];
        player.setToken(e.file, token)
      },
      "error": err => {
        console.log(err);
        console.log(err.status + "====" + err.statusText);

      }
    });
  });