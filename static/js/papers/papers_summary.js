$(document).ready(function() {
    $(".tdlink").click(function() {
        if ($(window).width() < 768) {
            window.location = $(this).data("href");
        }
    });
});
