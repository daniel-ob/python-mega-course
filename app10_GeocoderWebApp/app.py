from flask import Flask, render_template, request
import pandas
from geopy.geocoders import ArcGIS

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


@app.route("/")  # GET method by default
def index():
    """Displays the index page (homepage) accessible at '/'
    """
    return render_template("index.html")  # html files must be in templates folder


@app.route("/success", methods=['POST'])
def success():
    if request.method == "POST":
        file = request.files["file"]

        output_df = geocoder(file)
        print(output_df)
        if output_df is not None:
            msg = "Your file \"%s\" was successfully loaded" % file.filename
        else:
            msg = "Please make sure you have an address column in your CSV file!"

        return render_template("index.html", message=msg)


if __name__ == '__main__':
    app.debug = True
    app.run()
