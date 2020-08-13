/*  code is merged into template - solely for backup purpose
$('#exampleModalLong').on('shown.bs.modal', function (e) {
    e.preventDefault();
    var question_id = "{{ top_ten|index:forloop.counter0|index:3}}";
    $.get(location.origin + '/answers/'+question_id,
        {'question_id': question_id},
        function (response) {

            $('#response_msg').text(response.msg);
        }
    );
});*/
