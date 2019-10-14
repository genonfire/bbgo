$('#id_masterkey').keyup(function() {
    if ($(this).val().length == masterkey_length) {
        $('#masterkey_form').submit();
    }
});

$(document).ready(function(){
    $('#id_masterkey').attr('type', 'tel');
    $('#id_masterkey').focus();
});
