$(function () {

    $('#backBtn').click(function () {
        // 窗口返回上一页面
        window.history.back()
    });

    $('#payBtnDiv > button').click(function () {
        console.log(this);
        $('#payMsg').text('使用 ' + $(this).text()+ ' 正在完成支付...')
        $('#myModal').modal('show');

        orderNum = $(this).parent().attr('title');
        payType = $(this).attr('title');
        $.getJSON('/app/pay/'+orderNum+"/"+payType,function (data) {
            if(data.status == 'ok'){
                 $('#payMsg').text(data.msg);
                 setTimeout(function () {
                     $('#myModal').modal('hide');
                     window.open('/app/cart', target='_self');
                 },3000)

            }else{
                $('#payMsg').text(data.msg);
            }
        });

    })


})