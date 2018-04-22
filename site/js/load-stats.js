// Wie kan nog winnen is a collection of utilities to calculate and
// display what places teams of the Eredivisie can reach if everything
// goes perfectly.
// Copyright (C) 2017  Jochem Raat
// Copyright (C) 2017  Marien Raat

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

var insertStat = function (stat) {
    var row = $("<tr>");
    row.append($("<td>").text(stat.currentPlace + "."));
    row.append($("<td>").text(stat.teamName));
    var bestPlace = $("<td>").text(stat.bestPlace);
    row.addClass("best-place-" + stat.bestPlace);
    row.append(bestPlace);
    var worstPlace = $("<td>").text(stat.worstPlace);
    worstPlace.addClass("worst-place-" + stat.worstPlace);
    row.append(worstPlace);
    $("#places-table").append(row);
};

var insertWinner = function (winner) {
    var img = $("<img>").attr("alt", winner.teamName);
    img.addClass("winning-team");
    img.attr("src", winner.logoUrl);
    $("#winners div").append(img);
};

var insertLoser = function (loser) {
    var img = $("<img>").attr("alt", loser.teamName);
    img.addClass("losing-team");
    img.attr("src", loser.logoUrl);
    $("#losers div").append(img);
};


$.getJSON("/stats.json", function (stats) {
    stats.forEach(insertStat);
    var winners = stats.filter(function (stat) {
        return stat.bestPlace == 1;
    });
    winners.forEach(insertWinner);
    var losers = stats.filter(function (stat) {
        return stat.worstPlace >= 16;
    });
    losers.forEach(insertLoser);
});
