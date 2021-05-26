import justpy as jp
import pandas


data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data["Month"] = data["Timestamp"].dt.strftime("%Y-%m")
month_course_average = data.groupby(["Month", "Course Name"])["Rating"].mean().unstack()

# Areaspline-chart JSON from Highcharts documentation
# https://www.highcharts.com/docs/chart-and-series-types/areaspline-chart
chart_def = """
{
    chart: {
        type: 'areaspline'
    },
    title: {
        text: 'Average fruit consumption during one week'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor: '#FFFFFF'
    },
    xAxis: {
        categories: [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Fruit units'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ' units'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
    }]
}
"""


def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")

    # Add highchart
    hc = jp.HighCharts(a=wp, options=chart_def)
    # Set x axis values
    hc.options.xAxis.categories = list(month_course_average.index)

    # Construct series (list of dictionaries), each dictionary represents a line in the graph
    # using nested list comprehensions
    hc.options.series = [{
        "name": column,
        "data": [rating for rating in month_course_average[column]]
        } for column in month_course_average.columns]

    return wp


jp.justpy(app)
