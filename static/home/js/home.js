// $(function () {
//     topSwiper()
//     swiperMenu()
// })
//
//
// function topSwiper() {
//     var swiper = new Swiper('#topSwiper', {
//         direction: 'horizontal',
//         loop: true,
//         pagination: '.swiper-pagination',
//         paginationClickable: true,
//         effect:'cute',
//         autoplay:3000,
//         autoplayDisableOnInteraction:false
// })
// }
//
// function swiperMenu() {
//     var swiper = new Swiper('#swiperMenu', {
//         slidesPerView:3,
//         paginationClickable: true,
//         spaceBetween:2,
//         loop:false,
// })
// }
$(document).ready(function(){
    setTimeout(function(){
        swiper1()
        swiper2()
    },100)
})

function swiper1() {
    var mySwiper1 = new Swiper('#topSwiper', {
        direction: 'horizontal',
        loop: true,
        speed: 500,
        autoplay: 2000,
        pagination: '.swiper-pagination',
        control: true,
    });
};
function swiper2() {
    var mySwiper2 = new Swiper('#swiperMenu', {
        slidesPerView: 3,
        paginationClickable: true,
        spaceBetween: 2,
        loop: false,
    });
};
