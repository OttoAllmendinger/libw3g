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
            ttElement.show();
            setContent(ttElement);
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

    var getLevelSeries = function(levelLog, gameDuration) {
        var scaleTime = 1.0 / 60.0 / 1000.0;
        var scaledLog = [[0,0]].concat(
            $.map(levelLog, function(e, i) {
                return [[e[0]*scaleTime, e[1]]];
        }));

        scaledLog.push([
                    scaleTime*gameDuration*1000.0, 
                    scaledLog[scaledLog.length-1][1]
                ]);

        return scaledLog;
    }

    var getScoreSeries = function(killLog, deathLog, gameDuration) {
        var eventLog = $.map(killLog, function(e) {
                return [[e[0], 1]];
            }).concat($.map(deathLog, function(e) {
                return [[e[0], -1]];
            })).sort( function(a, b) {
                return a[0] - b[0];
            });

        var scoreLog = [[0,0]];
        var score = 0;
        $.each(eventLog, function(i, e) {
            score += e[1];
            scoreLog.push([e[0], score]);
        });

        var scaleTime = 1.0 / 60.0 / 1000.0;

        var scoreSequence = $.map(scoreLog, function(e, i) {
                return [e[1]];
        });
        
        var scaleScore = 100.0/Math.max(
                scoreSequence.max(),-scoreSequence.min());

        scaledScoreLog = $.map(scoreLog, function(e, i) {
                return [[ e[0]*scaleTime, e[1] ]]
        });

        scaledScoreLog.push( [
                scaleTime*gameDuration*1000.0,
                scaledScoreLog[scaledScoreLog.length-1][1]]);

        return scaledScoreLog;
    }



    $("td.playerStat").not(".absent").each(function(i) {
        var cell = $(this);
        setTooltip($(this), $("#ttPlayerStats"), function(tt) {
            var game = gameData[cell.dataset("game")];
            var player = game.players[cell.dataset("player")];
            tt.find(".heroName").text(dotaInfo[player.heroId].Name);


            /*
            var killDetails = "";

            $.each(player.killedPlayers, function(k,v) {
                if (killDetails) {
                    killDetails += ", ";
                }
                killDetails += k + ': ' + v;
            });

            tt.find(".killStats").text($.sprintf(
                "Kills: %d (%s)", player.kills, killDetails));
            */

            tt.find(".killStats").html(
                $.sprintf("Kills: <strong>%d</strong>", player.kills));


            /*
             * draw LevelChart
             */

            var levelSeries = [];
            var currentLevelSeries;

            $.each(game.players, function(name,playeri) {
                var newSeries = getLevelSeries(playeri.levelLog, game.duration);
                if (playeri==player) {
                    currentLevelSeries = newSeries;
                } else if (playeri.team==player.team) {
                    levelSeries.push({data: newSeries, color: "#5f5432"});
                } else {
                    levelSeries.push({data: newSeries, color: "#444444"});
                }
            });

            levelSeries.push({data: currentLevelSeries, color: "#ffffff"});

            var levelPlot = $.plot($(".chart.level"), levelSeries);


            /*
             * draw ScoreChart
             */

            var scoreSeries = [];
            var currentScoreSeries;

            $.each(game.players, function(name,playeri) {
                var newSeries = getScoreSeries(
                    playeri.killLog, playeri.deathLog, game.duration);
                if (playeri==player) {
                    currentScoreSeries = newSeries;
                } else if (playeri.team==player.team) {
                    scoreSeries.push({data: newSeries, color: "#5f5432"});
                } else {
                    scoreSeries.push({data: newSeries, color: "#444444"});
                }
            });

            scoreSeries.push({data: currentScoreSeries, color: '#ffffff'});

            var scorePlot = $.plot($(".chart.score"), scoreSeries);

        });
    });
}
