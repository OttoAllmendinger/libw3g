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

    $("td.playerStat").not(".absent").each(function(i) {
        var cell = $(this),
            game = gameData[cell.dataset("replay")],
            player = game.players[cell.dataset("player")];

        console.log(game);

        setTooltip($(this).children("img"), $("#ttPlayerStats"), function(tt) {
            tt.find(".heroName").text(dotaInfo[player.hero].Name);

            tt.find(".killStats").html(
                $.sprintf("Kills: <strong>%d</strong>", 
                    player.kill_log.length));

            tt.find(".deathStats").html(
                $.sprintf("Deaths: <strong>%d</strong>", 
                    player.death_log.length));

        });

        /*

        var details = $(this).closest("tr").next().find("div.gameDetails");
        var detailsChart = details.children(".chart");

        $(this).children("img").click(function() {
            details.slideToggle("fast", function() {
                showDetails(detailsChart, game, player);
            });
        });

        $(this).children("img").hover(function() {
            showDetails(detailsChart, game, player);
        });

        */
    });
}

init = function() {
    $.getJSON("/static/json/units-6.60.compact.json", function(data) {
        dotaInfo = data;
        initTooltips();
    });

    $.getJSON("/players?_+"+(new Date()).getTime(), function(data) {
        players = data;
    });

    $.getJSON("/gamedata?_="+(new Date()).getTime(), function(data) {
        gameData = data;
        initTooltips();
    });

<<<<<<< local

    // console.log(detailsElm.width(), detailsElm.height());

    if (detailsElm.width()>0 && detailsElm.height()>0) {
        $.plot(detailsElm, scoreSeries, {legend: {
                position: "sw",
                backgroundColor: 'null',
                labelBoxBorderColor: 'null',
            }
        });
    }
};
=======
}
>>>>>>> other
