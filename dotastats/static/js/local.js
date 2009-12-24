Array.prototype.max = function() {
        return Math.max.apply(null, this);
};

Array.prototype.min = function() {
        return Math.min.apply(null, this);
};



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
        var game = gameData[cell.dataset("game")];
        var player = game.players[cell.dataset("player")];

        setTooltip($(this).children("img"), $("#ttPlayerStats"), function(tt) {
            tt.find(".heroName").text(dotaInfo[player.heroId].Name);

            tt.find(".killStats").html(
                $.sprintf("Kills: <strong>%d</strong>", 
                    player.killLog.length));

            tt.find(".deathStats").html(
                $.sprintf("Deaths: <strong>%d</strong>", 
                    player.deathLog.length));

        });

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
    });
}


getScoreSeries = function(killLog, deathLog, gameDuration) {
    var eventLog = $.map(killLog, function(e) {
            return [[e[0], 1]];
        }).concat($.map(deathLog, function(e) {
            return [[e[0], -1]];
        })).sort(function(a, b) {
            return a[0] - b[0];
        }),

        scoreLog = [[0,0]],
        score = 0,
        ts = 0,
        lastTs = 0;

    $.each(eventLog, function(i, e) {
        ts = e[0];
        if ((ts-lastTs) > 100000) {
            scoreLog.push([ts-100000, score]);
        }
        score += e[1];
        scoreLog.push([ts, score]);
        lastTs = ts;
    });

    var scaleTime = 1.0 / 60.0 / 1000.0,
        scoreSequence = $.map(scoreLog, function(e, i) {
            return [e[1]];
        }),
        scaledScoreLog = $.map(scoreLog, function(e, i) {
            return [[ e[0]*scaleTime, e[1] ]]
        });

    scaledScoreLog.push( [
            scaleTime*gameDuration*1000.0,
            scaledScoreLog[scaledScoreLog.length-1][1]]);

    return scaledScoreLog;
}


showDetails = function(detailsElm, game, player) {
    var scoreSeries = [];

    $.each(game.players, function(name, playeri) {
        var newSeries = getScoreSeries(
            playeri.killLog, playeri.deathLog, game.duration);
        scoreSeries.push({data: newSeries, label:name, 
            color:playerColors[name]});
    });


    console.log(detailsElm.width(), detailsElm.height());

    if (detailsElm.width()>0 && detailsElm.height()>0) {
        $.plot(detailsElm, scoreSeries, {legend: {
                position: "sw",
                backgroundColor: 'null',
                labelBoxBorderColor: 'null',
            }
        });
    }
};


initColors = function() {
    playerColors = new Object();
    $(".playerName").each(function() {
            var playerName = $(this).dataset("player"),
                color = $.autocontrast(playerName, "dark");
            console.log(playerColors, playerColors[playerName]);
            if (playerColors[playerName]===undefined) {
                playerColors[playerName] = color;
            }

            $(this).css("color", playerColors[playerName]);
    });
    console.log("playerColors", playerColors);
}

init = function() {
    initTooltips();
    initColors();
}
