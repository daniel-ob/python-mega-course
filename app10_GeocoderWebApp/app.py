import os
import datetime

from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import ArcGIS

OUTPUT_FILES = "output_files"

# Create the application
app = Flask(__name__)


def geocoder(file):
    """
    Reads CSV file containing Address and returns a DataFrame with appended Latitude and Longitude columns
    :param file: csv file containing an "Address" or "address" column
    :return: DataFrame with added Latitude and Longitude columns. None if no address column found
    """
    df = pandas.read_csv(file)
    df.rename(columns={"address": "Address"}, inplace=True)

    if "Address" in df.columns:
        nom = ArcGIS()
        # Get Latitude and Longitude of each Address, add columns to df
        df["Latitude"] = df["Address"].apply(lambda x: nom.geocode(x).latitude)
        df["Longitude"] = df["Address"].apply(lambda x: nom.geocode(x).longitude)
        return df
    else:
        return None


def df_to_file(df):
    """Save df to CSV file. Create folder if doesn't exist
    """
    global output_file
    if not os.path.exists(OUTPUT_FILES):
        os.makedirs(OUTPUT_FILES)
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".csv"
    # Use os.path.join() for maximum portability
    output_file = os.path.join(OUTPUT_FILES, filename)
    df.to_csv(output_file, index=False)


@app.route("/")  # GET method by default
def index():
    """Displays the index page (homepage) accessible at '/'
    """
    return render_template("index.html", btn="")  # html files must be in templates folder


@app.route("/success", methods=['POST'])
def success():
    """Get user file, call geocoder and show output data in a table. Also show a download button.
    """
    if request.method == "POST":
        file = request.files["file"]

        output_df = geocoder(file)
        if output_df is not None:
            df_to_file(output_df)
            table = output_df.to_html(index=False)
            button = "download.html"
        else:
            table = "Please make sure you have an address column in your CSV file!"
            button = ""

        return render_template("index.html", table=table, btn=button)


@app.route("/download")
def download():
    """Download output dataframe as CSV file
    """
    return send_file(output_file, as_attachment=True, attachment_filename="yourfile.csv")


if __name__ == '__main__':
    app.debug = True
    app.run()
