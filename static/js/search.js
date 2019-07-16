$(document).ready(function() {
    main();
});

var main = function() {
    $("#search_box").keyup(function() {
        var text = { "text": $(this).val() }

        $.ajax({
            url: window.location.href + "search",
            type: "POST",
            data: JSON.stringify(text),
            contentType: "application/json",
            dataType: "json",
            success: function(result) {
                $("#search_result").empty()
                users = result.searchresult
                users.forEach(function(username) {
                    $("#search_result").append(username).append("<br>")
                });



            }
        })


        //alert($(this).val())
    });
}