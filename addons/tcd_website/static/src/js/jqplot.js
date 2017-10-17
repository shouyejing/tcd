$(document).ready(function () {
    if($(".columns").length){
        var s1 = [];
        var s2 = [];
        var ticks = [];

        $(".columns").each(function(index, value){
            s1.push(parseInt($(value).data("s1")));
            s2.push(parseInt($(value).data("s2")));
            ticks.push($(value).data("date"));

        });


        console.log(s1);
        console.log(s2);
        console.log(ticks);



        plot = $.jqplot('chart', [s1, s2], {
            seriesDefaults: {
                renderer:$.jqplot.BarRenderer,
                pointLabels: { show: true }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                }
            },
            legend:{
                renderer: $.jqplot.EnhancedLegendRenderer,
                show: true,
                placement: 'outside',
                location: 's',
                labels: ["budget  ", "actual  "],
                rendererOptions: {
                    numberRows: 1,
                    numberColumns: 2

                },
                marginTop: '40px',
                border: 'none',
            }
        });

    /*
        $('#chart').bind('jqplotDataHighlight',
            function (ev, seriesIndex, pointIndex, data) {
                $('#info').html('series: '+seriesIndex+', point: '+pointIndex+', data: '+data);
            }
        );

        $('#chart').bind('jqplotDataUnhighlight',
            function (ev) {
                $('#info').html('Nothing');
            }
        );
    */

    }



});
