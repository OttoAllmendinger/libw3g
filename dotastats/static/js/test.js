
init = function() {
    $.getJSON("/metadata?_="+(new Date()).getTime(), function(data) {
        console.log(data);
        $.each(data, function(i, e) {
            $('body').append(i + '<br/>');
        });
    });
}
