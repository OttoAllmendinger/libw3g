setTooltip = function(element, ttElement, setContent) {
    var xOffset = 10;
    var yOffset = 10;		

    var setPosition = function(x, y) {
        $(ttElement)
            .css("left", (xOffset+x)+"px")
            .css("top", (yOffset+y)+"px");
    }

    $(element).hover(function(e) {
            console.log("hover " + e);
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
    var tt_player = $("#tt_player");

    $("div.play_day").each(function(idx) {
        var play_day = $(this).dataset("play_day");
        $(this).find("th.player_name").each(function(idx) {
            var player_name = $(this).dataset("player").toString();
            setTooltip($(this), tt_player, function(tt) {
                $(tt).text(player_name);
            });
        });
    });


    $("td.player_stat").not(".absent").each(function(i) {
        var cell = $(this);
        setTooltip($(this), $("#tt_hero"), function(tt) {
            var heroId = gameData[cell.dataset("game")][cell.dataset("player")].heroId;
            // console.log(heroId);
            var heroImage = '/static/'+dotaInfo[heroId].Image;
            tt.children(".hero_image").attr("src", heroImage);
            tt.children(".hero_name").text(dotaInfo[heroId].Name);
        });
    });

}
