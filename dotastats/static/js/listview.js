init_data = function(units, players, games) {
    var tt = $(".tooltip#player_stats"),
        tt_playername = tt.children(".player_name"),
        tt_header = tt.children(".header"),
        tt_heroname = tt.children(".hero_name"),
        tt_items = tt.children(".items"),
        tt_stats = tt.children(".stats"),
        tt_slots = tt.find("img.item");

    console.log(tt);

    $("tr.game").each(function() {
        var replay_id = $(this).dataset("replay"),
                        game = games[replay_id];
        $(this).find("img").each(function() {
            var player_name = $(this).dataset("player"),
                player_data = game['players'][player_name];

            setTooltip($(this), tt, function() {
                // tt_playername.text(player_name);
                // tt_heroname.text(units[player_data.hero].Name);
                tt_stats.html($.sprintf(
                        "<b>%s</b> %d/%d/%d <br /> %s",
                        player_name,
                        player_data.kill_log.length,
                        player_data.death_log.length,
                        player_data.assist_log.length,
                        units[player_data.hero].Name ));

                var has_items = false,
                    i=0;

                $.each(tt_slots, function(j, slot) {
                    // $(slot).attr("src", "/static/images/dota/empty.png");
                    // $(slot).css("visibility", "hidden");
                    $(slot).hide();
                });

                $.each(player_data.inventory, function(j, item) {
                    if (item!==null) {
                        has_items = true;
                        // $(tt_slots[i]).css("visibility", "visible");
                        $(tt_slots[i]).show()
                        $(tt_slots[i]).attr("src", 
                            "/static/images/dota/"+units[item].Image);
                        i = i+1;
                    } 
                });

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
