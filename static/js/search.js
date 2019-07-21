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
    });

    //like function
    $('.likebutton').each(function() {
        $(this).click(function() {
            var post = { "postid": $(this).attr('id') }

            $.ajax({
                url: window.location.href + "like",
                type: "POST",
                data: JSON.stringify(post),
                contentType: "application/json",
                dataType: "json",
                success: function(result) {
                    var likeclass = ".like_" + result.postid
                    $(likeclass).empty()
                    likes = result.likes + " Likes"
                    $(likeclass).append(likes)
                    var buttonid = "#" + result.postid
                    $(buttonid).attr("disabled", true);
                }
            });

        });

    });
}