//异步获取
function ajax_get(url){
  var flag = arguments[1] ? arguments[1] : 0;
  if (flag == 0){
    $("#Refresh").show()
    $("#DialogSure").hide()
    $("#Refresh").attr("href", window.location.href)
  }else{
    $("#Refresh").hide()
    $("#DialogSure").show()
  }
  $.get(url,
    function(ret){
      if (ret.data.code == 0){
        if(ret.data.info){
          $("#DialogMain").html("<font color='green'>" + ret.data.info + "</font>")
        }else{
          $("#DialogMain").html("<font color='green'>操作成功，刷新页面可看效果！！！！</font>")
        }
      }else{
        if(ret.data.info){
          $("#DialogMain").html("<font color='red'>" + ret.data.info + "</font>")
        }else{
          $("#DialogMain").html("<font color='red'>操作失败！！！</font>")
        }
      }
  });
}

//异步操作
function ajax_post(send_url, json_data) {
  var flag = arguments[2] ? arguments[2] : 0;
  if (flag == 0){
    $("#Refresh").show()
    $("#DialogSure").hide()
    $("#Refresh").attr("href", window.location.href)
  }else{
    $("#Refresh").hide()
    $("#DialogSure").show()
  }
  $.ajax({
    type: "POST",
    url: send_url,
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(json_data),
    dataType: "json",
    success: function (ret) {
      if (ret.data.code == 0){
        if(ret.data.info){
          $("#DialogMain").html("<font color='green'>" + ret.data.info + "</font>")
        }else{
          $("#DialogMain").html("<font color='green'>操作成功，刷新页面可看效果！！！！</font>")
        }
      }else{
        if(ret.data.info){
          $("#DialogMain").html("<font color='red'>" + ret.data.info + "</font>")
        }else{
          $("#DialogMain").html("<font color='red'>操作失败！！！</font>")
        }
      }
    },
    error: function (data) {
      $("#DialogMain").html("<font color='red'>" + "未知错误请重试，或者联系刘礼!" + "</font>")
    }
  });
}

//获取check按钮的值
function get_checkbox_value(name){
    var arrChk=$("input[name='" + name + "']:checked");
    var id_list="";
    if(arrChk.length!=0)
    {
        for (var i=0;i<arrChk.length-1;i++)
        {
             id_list=id_list+arrChk[i].value+"__";
        }
        id_list = id_list+arrChk[arrChk.length-1].value;
    }
    return id_list
}

function confirm_option(url){
  var r=confirm("你的操作将不可恢复，是否继续?")
  if (r==true){
    ajax_get(url)
  }else{
    $("#DialogMain").html("<font color='red'>你已经取消了操作！</font>")
  }
}

function post(url, json_data){
  $.post(url,
    JSON.stringify(json_data),
    function(data,status){
      if(data.status == "success"){
        alert("操作成功，刷新页面查看结果！")
      }else{
        alert("操作失败！"+data.message)
      }
  });
}
