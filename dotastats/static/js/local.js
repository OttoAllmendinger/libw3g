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

initTooltips = function() {
    var tt_player = $("#ttPlayer");

    $("div.playDay").each(function(idx) {
        var play_day = $(this).dataset("playDay");
        $(this).find("th.playerName").each(function(idx) {
            var player_name = $(this).dataset("player").toString();
            setTooltip($(this), tt_player, function(tt) {
                $(tt).text(player_name);
            });
        });
    });


    $("td.playerStat").not(".absent").each(function(i) {
        var cell = $(this);
        setTooltip($(this), $("#ttPlayerStats"), function(tt) {
            var player = gameData[cell.dataset("game")]
                            .players[cell.dataset("player")];
            tt.find(".heroName").text(dotaInfo[player.heroId].Name);


            var killDetails = "";

            $.each(player.killedPlayers, function(k,v) {
                if (killDetails) {
                    killDetails += ", ";
                }
                killDetails += k + ': ' + v;
            });

            /*
            tt.find(".killStats").text($.sprintf(
                "Kills: %d (%s)", player.kills, killDetails));
            */
            tt.find(".killStats").html(
                $.sprintf("Kills: <strong>%d</strong>", player.kills))
        });
    });

}
