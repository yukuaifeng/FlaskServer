$("#query-form").submit(function (e) {
        var kind = $("#kind").val();
        var rank = $("#Rank").val();
        var score = $("#Score").val();

        $.ajax({
            url: /query/,
            type: 'get',
            dataType: 'json',
            data: {'kind': kind, 'rank': rank, 'score': score},
            success: function (data) {

            },
            error: function (data) {
                alert('请求失败')
            }


        })

    })

// function query_submit() {
//     var kind = $("#kind").val();
//     var rank = $("#Rank").val();
//     var score = $("#Score").val();
//     $.post('/query/',
//         {'kind': kind, 'rank': rank, 'score': score},
//         function (msg) {
//             alert(msg.code)
//     });
// }