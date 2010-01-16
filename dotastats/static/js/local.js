setTooltip = function(element, ttElement, setContent) {
    var xOffset = 10;
    var yOffset = 10;		

    var setPosition = function(x, y) {
        $(ttElement)
            .css("left", (xOffset+x)+"px")
            .css("top", (yOffset+y)+"px");
    }

    $(element).hover(function(e) {
            setPosition(e.pageX, e.pageY);
            setContent(ttElement);
            ttElement.show();
        }, function() {
            ttElement.hide();
        }
    );

    $(element).mousemove(function(e) {
        setPosition(e.pageX, e.pageY);
    });
}

init_data = function(units, players, games) {
    console.log(arguments);
    var tt = $(".tooltip#player_stats"),
        tt_header = tt.children(".header"),
        tt_items = tt.children(".items");

    $("tr.game").each(function() {
        var replay_id = $(this).dataset("replay"),
                        game = games[replay_id];
        $(this).find("span.player").each(function() {
            var player_name = $(this).dataset("player"),
                player_data = game['players'][player_name],
                image = $(this).children("img.hero_image");

            setTooltip($(this), tt, function() {
                tt.html($.sprintf("<b>%s (%s)</b>",
                        player_name, units[player_data.hero].Name));
            });
        });
    });
}

init = function() {
    $.getAllJSON(
            "/static/json/units-6.60.compact.json", 
            "/json/players?_="+(new Date()).getTime(),
            "/json/gamedata?_="+(new Date()).getTime(),
            init_data);
}
