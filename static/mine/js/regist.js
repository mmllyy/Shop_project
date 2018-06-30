function showError(msg,isUseLable) {
    var errorP = this.parentElement.nextElementSibling
            errorP.innerText = isUseLable?this.title+msg:msg;
            $(errorP).fadeIn();
            // 设置input-group 存在错误
            $(this.parentElement).addClass('has-error');
            this.value=''
            $(this).focus(function () {
                 $(errorP).fadeOut();
                 $(this.parentElement).removeClass('has-error');
            });
}

$(function () {
    $('input').blur(function () {
        if(this.value.trim().length == 0){
            showError.call(this,'不能为空',true)
            return
        }
        if (this.name == 'username' &&
            this.value.trim().length < 10) {
            showError.call(this, this.placeholder,true);
            return
        }
        if (this.name == 'passwd2') {
            var passwd1 = $('input[name=passwd]').val()
            console.log('口令1： ', passwd1);
            if (this.value.trim() != passwd1.trim())
                showError.call(this, '两次口令不相同！', false);
            return
        }
        if (this.name == 'phone') {
            phone = this.value.trim();
            if (phone.length != 11) {
                showError.call(this, '请输入11位的手机号', false);
                return;
            }
            if (! /1[3-9]\d{9}/.test(phone)) {
                showError.call(this, '手机号无效',false);
                return;
            }

        }
    })
})


function submitForm() {
    var inputs = $('input')
    // 验证是否为空的
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs.get(i)
        if ($(input).val().trim() == '') {
            $(input).parent().addClass('has-error');
            $(input).parent().next().fadeIn()
            return
        } else {
            $(input).parent().removeClass('has-error');
            $(input).parent().next().fadeOut()
        }
    }
    // 提交注册
    $('form').submit()
}