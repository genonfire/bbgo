$('#id_portrait').on('change', function() {
    var file = this.files[0];
    var type_validator = ["image/gif", "image/jpeg", "image/png"];
    if ($.inArray(file["type"], type_validator) < 0) {
        msg = gettext("Please select correct image.");
        $("#id_portrait").replaceWith($("#id_portrait").val('').clone(true));
        alert(msg);
    }
    else if (file.size > portrait_limit) {
        var sizelimit = portrait_limit / 1024 + 'KB';
        msg = gettext("Selected image is too big. size limit: ") + sizelimit;
        $("#id_portrait").replaceWith($("#id_portrait").val('').clone(true));
        alert(msg);
    }
});
