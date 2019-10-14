function register_spam_ip(ip) {
    if (ip.length < 7) {
        alert(gettext("Please input correct IP address."));
        return;
    }

    if (confirm(gettext("Are you sure to register this IP address to spam?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/spams/register_ip/",
            data: {
                ip: ip
            },
            success: function(data) {
                toast(gettext("Saved successfully."));
            },
            error: function(data) {
                if (data.status == 412) {
                    toast(gettext("Already exist."));
                }
                else if (data.status == 500) {
                    toast(gettext("Please input correct IP address."));
                }
                else {
                    alert(gettext('Error!'));
                }
            }
        });
    }
}

$('#id_category').change(function() {
    category = $(this).val();
    url = dashboard_post_url.replace(/\/bb\//, '\/' + category +'\/');
    location.href = url;
});
