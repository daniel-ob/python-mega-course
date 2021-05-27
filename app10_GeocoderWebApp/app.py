from flask import Flask, render_template, request

# Create the application
app = Flask(__name__)


@app.route("/")  # GET method by default
def index():
    """Displays the index page (homepage) accessible at '/'
    """
    return render_template("index.html")  # html files must be in templates folder


@app.route("/success", methods=['POST'])
def success():
    if request.method == "POST":
        file = request.files["file"]
        print(file)
        return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
