$('#id_category').change(function() {
    category = $(this).val();
    url = dashboard_article_url.replace(/\/99999\//, '\/' + category +'\/');
    location.href = url;
});
