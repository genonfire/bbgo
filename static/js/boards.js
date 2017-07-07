function search() {
    var type = $('#searchType').val();
    var word = $('#searchWord').val();
    if (!word) {
        alert("검색어를 입력하세요.");
        return;
    }
    // var url = "{% url 'search issue' search_range='search_range' search_type='type' search_word='word' nolook='nolook' %}".replace(/search_range/, search_range).replace(/type/, type).replace(/word/, word).replace(/nolook/, nolook).replace(/http:\/\//, '').replace(/https:\/\//, '').replace(/twitter.com\//, '').replace(/facebook.com\//, '');
    // if (url.substr(-1) == '/') {
    //     url = url.slice(0, -1);
    // }
    // location.href = url;
}

function cacnel() {
    if (confirm("글 작성을 취소하고 나가시겠습니까?")) {
        history.back(1);
    }
}

function onKeyPress(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        search();
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

$(document).ready(function() {
  $('pre').each(function(i, block) {
    hljs.highlightBlock(block);
  });
});
