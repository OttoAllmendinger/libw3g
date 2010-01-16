jQuery.getAllJSON = function() {
    var n = arguments.length,
        cbArguments = Array(n-1),
        unfetched = n-1;
        callback = arguments[n-1];

    $.each(arguments, function(i,a) {
        if (i<(n-1)) {
            $.getJSON(a, function(data) {
                cbArguments[i] = data;
                unfetched -= 1;
                if (unfetched===0) {
                    callback.apply(null, cbArguments);
                }
            });
        }
    });
};
