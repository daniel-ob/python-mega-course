from flask import Flask, render_template

app = Flask(__name__)


# Homepage
@app.route("/")
def home():
    return render_template("home.html")  # file must be in templates/ folder


# About page
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)
