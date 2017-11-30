function delete_vault(url) {
    if (confirm(gettext("Are you sure to delete?"))) {
        location.href = url;
    }
}

function empahsis(id) {
    tagname = '#vault_' + id;
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
        url: "/vaults/save/",
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

function extend_expiry() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/vaults/extend_expiry/",
        success: function(data) {
            toast(gettext("Extended."));
            expiry = data[0];
        },
        error: function(data) {
            toast(gettext('Already expired.'));
            location.reload();
        }
    });
}

$(function() {
    if (enable_masterkey) {
        function padding(val) {
            return val > 9 ? val : "0" + val;
        }
        var interval = setInterval(function(){
            expiry_min = parseInt(--expiry / 60, 10);
            expiry_sec = expiry % 60
            $('#expiry_min').html(padding(expiry_min));
            $('#expiry_sec').html(padding(expiry_sec));

            if (expiry <= 0) {
                clearInterval(interval);
                location.reload();
            }
        }, 1000);
    }
    $('.vault_number span').click(function() {
        text = $(this).text();
        if (text) {
            number = text.split('-').join('');
            $('#copyslave').val(number);
            $('#copyslave').show();
            $('#copyslave').select();
            document.execCommand("Copy");
            $('#copyslave').hide();
            toast(gettext("Copied to clipboard."), 1000);
        }
    });

    if ($("#sort_items").length) {
        $("#sort_items").sortable({containment: "#sort_container"});
        $("#sort_items").disableSelection();
    }
});
