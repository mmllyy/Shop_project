$(function () {
    $('#allType').click(function () {

        // 获取分类的<span>内显示图标的子标签<span><span></span></span>
        $(this.lastChild).toggleClass('glyphicon-chevron-down')

        if($('#typeDiv')[0].style.display == 'block'){
            $('#typeSortDiv').css('display', 'none');
            $('#typeDiv').css('display', 'none');
            return;
        }

        $('#typeSortDiv').css('display', 'block');
        $('#typeDiv').css('display', 'block');

        //还原排序
        $('#goodsSort :last-child').removeClass('glyphicon-chevron-down');
        $('#sortDiv').css('display', 'none');
    });

    $('#goodsSort').click(function () {
        // this -> 被点击的DOM对象
        $(this.lastChild).toggleClass('glyphicon-chevron-down')
         console.log($('#sortDiv')[0].style.display);
         if($('#sortDiv')[0].style.display == 'block'){
            $('#typeSortDiv').css('display', 'none');
            $('#sortDiv').css('display', 'none');
            return;
        }

        $('#typeSortDiv').css('display', 'block');
        $('#sortDiv').css('display', 'block');

        //还原分类
        $('#typeDiv').css('display', 'none');
        $('#allType :last-child').removeClass('glyphicon-chevron-down');
    })
    
    $('#typeSortDiv').click(function () {
        $(this).css('display', 'none');

        $('#allType :last-child').removeClass('glyphicon-chevron-down');
        $('#goodsSort :last-child').removeClass('glyphicon-chevron-down');
    })
});