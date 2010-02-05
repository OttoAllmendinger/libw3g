init_data = function(units, players, gamedata) {
    console.log(units);
    console.log(players);
    console.log(gamedata);

    // console.log($("td.inventory"));
    // console.log($("td.inventory").children("img.item"));

    var tooltip = $("#tooltip");

    $("td.inventory").children(".item").each(function() {
            var item_id = $(this).dataset("item_id"),
                item_data = units[item_id];
            if (item_data) {
                setTooltip($(this), tooltip, function(e) {
                    tooltip.text($.sprintf(
                            "%s (%d)", item_data.Name, item_data.Cost));
                });
            }
    });


    $("img.hero").each(function() {
            var hero_id = $(this).dataset("hero_id"),
                hero_data = units[hero_id];
            if (hero_data) {
                setTooltip($(this), tooltip, function(e) {
                    tooltip.text($.sprintf(
                            "%s", hero_data.Name))
                });
            }
    });


    /*

    $("tr.player_stats").each(function() {
            var player = $(this).dataset("player"),
                kill_log = gamedata.players[player].kill_log,
                td_kill = $(this).children("td.kills");
            setTooltip(td_kill, tooltip, function(e) {
                $.each(kill_log, function(i, e) {
                    console.log(findplayer_id(gamedata.players, e[1]));
                });
            })
    });

    */
                
}

load_game = function(replay_id) {
    $.getAllJSON(
            "/static/json/units-6.60.compact.json", 
            "/json/players?_="+(new Date()).getTime(),
            "/json/gamedata?replay_id=" 
                + replay_id 
                + "&_="+(new Date()).getTime(),
            init_data);
}
