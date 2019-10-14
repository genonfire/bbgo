function toast(message, delay=1500) {
    var remove_toast = function(){
        $('#toast_popup').remove();
        $('#popup_overlay').remove();
    };
    remove_toast();
    $('body').append('<div id="popup_overlay"></div><div id="toast_popup"></div></div>');
    $('#toast_popup').click(remove_toast);
    $('#toast_popup').html(message).show().delay(delay).fadeOut(300, remove_toast);
}
