from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker


def plot(df, file):
    """Shows a plot of motion-detector log (DataFrame). Also saves this plot in a html file"""
    # create figure object
    p = figure(x_axis_type="datetime", plot_height=300, sizing_mode="stretch_width", title="Motion Detector Graph")
    # remove minor ticks of y axis
    p.yaxis.minor_tick_line_color = None
    # only 0 and 1 values in y axis
    p.yaxis.ticker = FixedTicker(ticks=[0, 1])
    # hide y grid
    p.ygrid.visible = False

    # add rectangles (for each one: bottom=0, top=1)
    p.quad(left=df["Enter"], right=df["Exit"], bottom=0, top=1, color="green")

    # prepare the output file
    output_file(file)

    # write the plot in the figure object
    show(p)
