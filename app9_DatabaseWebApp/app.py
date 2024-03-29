from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from send_mail import send_mail

# Create the application
app = Flask(__name__)
# Set URI for the database to be used: dialect[+driver]://user:password@host/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_survey'
# Create database object for the application
db = SQLAlchemy(app)


class Data(db.Model):
    """Table to store survey data
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


@app.route("/")  # GET method by default
def index():
    """Displays the index page (homepage) accessible at '/'
    """
    return render_template("index.html")  # html files must be in templates folder


@app.route("/success", methods=['POST'])
def success():
    """Stores data into database and displays the success page
    """
    if request.method == "POST":
        email = request.form['email']
        height = request.form['height']
        # print(request.form)
        print(email, height)

        # If email does not yet exists
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            # Add data to database
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()

            average_height = round(db.session.query(func.avg(Data.height)).scalar())  # int value
            count = db.session.query(Data.height).count()
            # print(average_height, count)

            send_mail(email, height, average_height, count)
            return render_template("success.html")
        else:
            return render_template("index.html", message="This email already exists in our database")


if __name__ == '__main__':
    # create all tables
    db.create_all()

    app.run(debug=True)
