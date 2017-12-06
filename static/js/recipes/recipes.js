function empahsis(id) {
    tagname = '#' + id;
    bgcolor = $(tagname).css('background-color');
    if (bgcolor == 'rgba(0, 0, 0, 0)') {
        $(tagname).css('background-color', '#eee');
    }
    else {
        $(tagname).css('background-color', 'rgba(0, 0, 0, 0)');
    }
}

function save_order() {
    var order = []
    $('#sort_items div').each(function(i) {
        id = $(this).attr('id');
        if (id) {
            order.push(id);
        }
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/recipes/save/",
        data: {
            order: order
        },
        success: function(data) {
            toast(gettext("Saved successfully."));
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

function what_today(category) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/recipes/what_today/",
        data: {
            category: category
        },
        success: function(data) {
            id = '#' + data;
            $('html,body').animate({ scrollTop: $(id).offset().top - 30 }, 'fast');
        },
        error: function(data) {
            toast(gettext('Error!'));
        }
    });
}

function scroll_top() {
    $('html,body').animate({ scrollTop: 0 }, 'fast');
}

$(function() {
    if ($("#sort_items").length) {
        $("#sort_items").sortable({containment: "#sort_container"});
        $("#sort_items").disableSelection();
    }
});
