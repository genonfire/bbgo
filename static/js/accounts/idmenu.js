function show_popup(e, data, width, marginX, marginY) {
    var top = e.clientY + $(document).scrollTop() + marginY;
    var left = e.clientX - (width - 10) + $(document).scrollLeft();
    if (e.clientX - (width - 10) < marginX)
        left = marginX + $(document).scrollLeft();

    $('<div/>', {
        id: 'popup_frame',
        class: 'popup_frame',
        html: data,
        style: "width:" + width + "px;position:absolute;top:" + top + "px;left:" + left + "px;"
    }).appendTo('body');
    $('#popup_frame').on('mousedown', function(e) {
        e.stopPropagation();
    })
    $('body').on('mousedown', function(e) {
        $('#popup_frame').remove();
        $('body').off('mousedown');
    })
}

function id_menu(e, user) {
    var userinfo_text = gettext("user info");
    var userinfo_url = url_userinfo.replace(/\/bb\//, '\/' + user +'\/');
    var userarticle_text = gettext("Show user article");
    var userarticle_url = url_userarticle.replace(/\/bb\//, '\/' + user +'\/');
    var userreply_text = gettext("Show user reply");
    var userreply_url = "#";
    var message_text = gettext('Send message');
    var message_url = "#";
    var data = '<table width="100%"><tr><td><a href="' + userinfo_url + '">' + userinfo_text + '</a>' + '</td></tr><tr><td><a href="' + userarticle_url + '">' + userarticle_text + '</a></td></tr><tr><td><a href="' + userreply_url + '">' + userreply_text + '</a></td></tr><tr><td><a href="' + message_url + '">' + message_text +'</a></td></tr></table>';

    show_popup(e, data, 90, 20, 20);
}
