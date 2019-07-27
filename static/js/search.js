$(document).ready(function () {
    main();
});


var main = function () {

    $("#search_box").keyup(function () {
        var text = {
            "text": $(this).val()
        }
        $.ajax({
            url: window.location.origin + "/search",
            type: "POST",
            data: JSON.stringify(text),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
                $("#search_result").empty().append("<div style='font-weight:500;margin-bottom:10px;'>Search Results:</div>");

                users = result.searchresult
                users.forEach(function (result) {

                    userid = result.split('-')[0]
                    username = result.split('-')[1]

                    var link = $('<a>', {
                        text: username,
                        title: username,
                        href: window.location.origin + '/profile/' + userid
                        //click: function() { GotoProfile(userid); return false; }
                    })

                    $("#search_result").append(link).append("<br>")


                });
            }
        })
    });



    //like function
    $('.likebutton').each(function () {
        $(this).click(function () {
            var post = {
                "postid": $(this).attr('id')
            }

            $.ajax({
                url: window.location.origin + "/like",
                type: "POST",
                data: JSON.stringify(post),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {
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

  

    //like function
    $('.status_button').each(function () {
        var userid = $(this).attr('id')
        var statusid = 'status_' + userid
        var status = $("#" + statusid).html() //$("#" + statusid).val()
        if (status == 1) {
            //$("#" + userid).prop('text', 'Accept friend')
            $("#" + userid).html('Accept friend');

        }
        $(this).click(function () {
            // 2 means to become friends
            var result = {
                "userid": userid,
                "status": "2"
            }
            $.ajax({
                url: window.location.origin + "/updatestatus",
                type: "POST",
                data: JSON.stringify(result),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {
                    $("#" + result.userid).html('Friends now!');
                }
            });

        });

    });
}