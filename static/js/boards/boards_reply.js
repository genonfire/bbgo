function write_reply(id) {
    // text = $('#reply_text').val();
    // var formData = new FormData();
    // formData.append('file', $('#reply_image').files[0]);
    // var formData = new FormData(document.getElementById("form_reply"));
    // formData.append("label", "file");
    var data = new FormData($('#form_reply').get(0));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_reply/",
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#reply_text').val = '';
        },
        error: function(data) {
            alert(data);
        }
    });
}

$('#reply_image').on('change', function() {
    var file = this.files[0];
    if (file.size > reply_image_limit) {
        var sizelimit = reply_image_limit / 1024 / 1024 + 'MB';
        msg = gettext("Selected image is too big. size limit: " + sizelimit);
        $("#reply_image").replaceWith($("#reply_image").val('').clone(true));
        alert(msg);
    }
});
