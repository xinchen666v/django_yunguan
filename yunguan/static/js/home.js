// 确保DOM完全加载后再运行JavaScript代码
document.addEventListener('DOMContentLoaded', function () {
    var slideIndex = 0;
    showSlides();

    function showSlides() {
        var i;
        var slides = document.getElementsByClassName("mySlides");
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        slideIndex++;
        if (slideIndex > slides.length) { slideIndex = 1 }
        slides[slideIndex - 1].style.display = "block";
        // 每8秒更换一次图片
        setTimeout(showSlides, 8000);
    }
});
