
var insertStat = function (stat) {
    var row = $("<tr>");
    row.append($("<td>").text(stat.teamName));
    var place = $("<td>").text(stat.bestPlace);
    row.addClass("place-" + stat.bestPlace);
    row.append(place);
    $("#places-table").append(row);
};

var insertWinner = function (winner) {
    var img = $("<img>").attr("alt", winner.teamName);
    img.addClass("winning-team");
    img.attr("src", winner.logoUrl);
    $("#winners div").append(img);
};

$.getJSON("/stats.json", function (stats) {
    stats.forEach(insertStat);
    var winners = stats.filter(function (stat) {
        return stat.bestPlace == 1;
    });
    winners.forEach(insertWinner);
});
