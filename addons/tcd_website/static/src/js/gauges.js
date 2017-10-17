$(document).ready(function () {

    // Colors of the gauge
    var red = "#FF0000";
    var yellow = "#FFFF00";
    var green = "#32CD32";
    $(".project-indicator-average").each(function(index, project){
        new JustGage({
            id: project.id,
            value: $(project).data("indicator-average"),
            min: 0,
            max: 5,
            decimals: 1,
            title: "",
            levelColors: [
              red,
              yellow,
              green,
            ]
        });
    });

    $(".indicator-rating").each(function(index, indicator){
        new JustGage({
            id: indicator.id,
            value: $(indicator).data("indicator-rating"),
            min: 0,
            max: 5,
            title: $(indicator).data("indicator-name"),
            label: $(indicator).data("indicator-rating-label"),
            levelColors: [
              red,
              yellow,
              green,
            ]
        });
    });

});
