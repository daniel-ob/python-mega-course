from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker
from bokeh.models import HoverTool, ColumnDataSource


def plot(df, file):
    """Shows a plot of motion-detector log (DataFrame). Plot is also saved in a html file"""

    # add string version of Enter and Exit columns (use datetime formatting)
    df["Enter_string"] = df["Enter"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["Exit_string"] = df["Exit"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # for HoverTool function we need to convert DataFrame into a ColumnDataSource
    cds = ColumnDataSource(df)

    # create figure object
    p = figure(x_axis_type="datetime", plot_height=300, sizing_mode="stretch_width", title="Motion Detector Graph")
    # remove minor ticks of y axis
    p.yaxis.minor_tick_line_color = None
    # only 0 and 1 values in y axis
    p.yaxis.ticker = FixedTicker(ticks=[0, 1])
    # hide y grid
    p.ygrid.visible = False

    # define tooltips label and data
    hover = HoverTool(tooltips=[("Enter", "@Enter_string"), ("Exit", "@Exit_string")])
    # add hover to the figure object
    p.add_tools(hover)

    # add rectangles using cds
    p.quad(left="Enter", right="Exit", bottom=0, top=1, color="green", source=cds)

    # prepare the output file
    output_file(file)

    # write the plot in the figure object
    show(p)
