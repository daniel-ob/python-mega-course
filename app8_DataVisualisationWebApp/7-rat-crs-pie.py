import justpy as jp
import pandas

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
cnt_rat_crs = data.groupby(["Course Name"])["Rating"].count()

# Pie-chart JSON from Highcharts documentation
# https://www.highcharts.com/docs/chart-and-series-types/pie-chart
chart_def = """
{
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Number of Ratings by Course'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    accessibility: {
        point: {
            valueSuffix: ''
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.y}'
            }
        }
    },
    series: [{
        name: 'Ratings',
        colorByPoint: true,
        data: [{
            name: 'Chrome',
            y: 61.41,
            sliced: true,
            selected: true
        }, {
            name: 'Internet Explorer',
            y: 11.84
        }, {
            name: 'Firefox',
            y: 10.85
        }, {
            name: 'Edge',
            y: 4.67
        }, {
            name: 'Safari',
            y: 4.18
        }, {
            name: 'Sogou Explorer',
            y: 1.64
        }, {
            name: 'Opera',
            y: 1.6
        }, {
            name: 'QQ',
            y: 1.2
        }, {
            name: 'Other',
            y: 2.61
        }]
    }]
}
"""


def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")

    # Add highchart. Justpy will parse JSON as dictionary
    hc = jp.HighCharts(a=wp, options=chart_def)

    # Set graph data
    hc.options.series[0].data = [{
        "name": course_name,
        "y": ratings
    } for course_name, ratings in zip(list(cnt_rat_crs.index), list(cnt_rat_crs))]

    return wp


jp.justpy(app)
