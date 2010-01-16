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
            try {
                setContent(ttElement);
            } catch(ex) { }
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
        tt_heroname = tt.children(".hero_name"),
        tt_items = tt.children(".items"),
        tt_inventory = tt.children("#inventory"),
        tt_slots = tt_inventory.find("img");

    console.log(tt);
    console.log(tt_inventory);

    $("tr.game").each(function() {
        var replay_id = $(this).dataset("replay"),
                        game = games[replay_id];
        $(this).find("div.player").each(function() {
            var player_name = $(this).dataset("player"),
                player_data = game['players'][player_name],
                image = $(this).children("img.hero_image");

            setTooltip($(this), tt, function() {
                tt_heroname.text(units[player_data.hero].Name);
                var has_items = false;

                $.each(player_data.inventory, function(i, item) {
                    if (item!==null) {
                        has_items = true;
                        $(tt_slots[i]).css("visibility", "visible");
                        $(tt_slots[i]).attr("src", 
                            "/static/images/dota/"+units[item].Image);
                    } else {
                        $(tt_slots[i]).css("visibility", "hidden");
                    }
                });

                if (has_items===false) {
                    tt_inventory.hide();
                } else {
                    tt_inventory.show();
                }

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
