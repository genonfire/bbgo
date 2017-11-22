$('#id_category').change(function() {
    category = $(this).val();
    url = dashboard_post_url.replace(/\/bb\//, '\/' + category +'\/');
    location.href = url;
});
