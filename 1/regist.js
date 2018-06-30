$(function () {
    $('input').blur(function () {
        if(this.value.trim().length == 0){
            var errorP = this.parentElement.nextElementSibling
            errorP.innerText =this.title +' 不能为空 ';
            $(errorP).fadeIn();
            // 设置input-group 存在错误
            $(this.parentElement).addClass('has-error');

            $(this).focus(function () {
                 $(errorP).fadeOut();
                 $(this.parentElement).removeClass('has-error');
            });
        }
    })
})