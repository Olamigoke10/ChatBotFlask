from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Set the database URI for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))



@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        user_name = request.form["user_name"]
        email = request.form["email"]
        password = request.form["password"]

        form = Form(first_name=first_name, last_name=last_name, user_name=user_name,
                    password=password, email=email)

        db.session.add(form)
        db.session.commit()

        return redirect(url_for('login'))


    return render_template("signup.html")



@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
