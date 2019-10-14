function new_category() {
    name = $('#new_category_name').val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/recipes/new_category/",
        data: {
            name: name
        },
        success: function(data) {
            $('#new_category_name').val('');
            $('#sort_container').html(data);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

function delete_category(id) {
    if (confirm(gettext("Are you sure to delete?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/recipes/delete_category/",
            data: {
                id: id
            },
            success: function(data) {
                $('#sort_container').html(data);
            },
            error: function(data) {
                alert(gettext('Error!'));
            }
        });
    }
}

function save_category() {
    var order = []
    $('#sort_items li').each(function(i) {
        id = $(this).attr('id');
        name = $('#' + id + ' input').val();
        if (id) {
            order.push(id + ':' + name);
        }
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/recipes/save_category/",
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

$(function() {
    if ($("#sort_items").length) {
        $("#sort_items").sortable({containment: "#sort_container"});
        $("#sort_items").disableSelection();
    }
});
