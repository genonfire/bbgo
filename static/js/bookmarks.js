function toggle_bookmark(app, id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/toggle_bookmark/",
        data: {
            app: app,
            id: id
        },
        success: function(datain) {
            $('#header_star').attr("src", datain);
        },
        error: function(data) {
            alert(gettext("Error!"));
        }
    });
}