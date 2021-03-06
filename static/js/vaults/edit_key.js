$('#masterkey_form').submit(function(e) {
    current_key = $('#id_current_key').val(); 
    masterkey1 = $('#id_masterkey').val();
    masterkey2 = $('#id_masterkey2').val();
    if (masterkey1.length != masterkey_length || current_key.length != masterkey_length) {
        e.preventDefault();
        alert(gettext("Mind the chracter length limitation."));
        return;
    }
    if (masterkey1 != masterkey2) {
        e.preventDefault();
        alert(gettext("Master keys are different each other."));
        return;
    }
    if (masterkey1 == current_key) {
        e.preventDefault();
        alert(gettext("New masker key is same as current key."));
        return;
    }
    var isnum = /^\d+$/.test(masterkey1);
    if (!isnum) {
        e.preventDefault();
        alert(gettext("Number only!"));
        return;
    }
});

$(document).ready(function(){
    $('#id_current_key').attr('type', 'tel');
    $('#id_masterkey').attr('type', 'tel');
    // $('#id_masterkey2').attr('type', 'tel');
});
