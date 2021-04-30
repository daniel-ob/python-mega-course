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
    """Prints collected data and displays the success page (accessible at 'success')
    """
    if request.method == "POST":
        email = request.form['email']
        height = request.form['height']
        # print(request.form)
        print(email, height)
        return render_template("success.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
