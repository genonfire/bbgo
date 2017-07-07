function cacnel() {
    if (confirm("글 작성을 취소하고 나가시겠습니까?")) {
        history.back(1);
    }
}

$('#edit_article_form').submit(function(e) {
    url = $('#id_reference').val().replace(/htp:\/\//, '').replace(/http;\/\//, '');
    if (url) {
        if (!/^(https?|http):\/\//.test(url)) {
            $('#id_reference').val("http://" + url);
        }
    }

    subject = $('#id_subject').val();
    content = $('#id_content').val();

    if (!subject) {
        e.preventDefault();
        alert("제목을 입력해 주세요.");
        return;
    }
    if (!content || content == "<p><br></p>") {
        e.preventDefault();
        alert("내용을 입력해 주세요.");
        return;
    }

    $(window).unbind('beforeunload');
});

$(window).bind('beforeunload', function(){
    return '글 작성을 취소하고 나가시겠습니까?';
});
