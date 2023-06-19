window.onload = function Dialog1() {
    $("#open").click(function(){
        document.getElementById('dialog_1').show()
    })
    $("#close").click(function(){
        document.getElementById('dialog_1').close()
    })

}




function addLike(){
    $('#like').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'like': 1
            },
            'success': function(data){
                document.getElementById('likes').innerHTML = data['like_amount'];
            }
        })
    })
}


$(document).ready(function(){
    addLike();

    $.ajax($('#like').data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_like': 1
        },
    })


})