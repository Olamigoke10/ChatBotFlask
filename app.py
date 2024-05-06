from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Set the database URI for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"

# Set the secret key
app.config['SECRET_KEY'] = 'hellogoke'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)



@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        user_name = request.form["user_name"]
        email = request.form["email"]
        password = request.form.get('password')

        # hash the password
        hashed_password = generate_password_hash(password)

        form = Form(first_name=first_name, last_name=last_name, user_name=user_name,
                    password=hashed_password, email=email)

        db.session.add(form)
        db.session.commit()

        return redirect(url_for('login'))


    return render_template("signup.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')

        form = Form.query.filter_by(email=email).first()

        if form:
            if check_password_hash(form.password, password):
                flash("Login Successful", category="success")
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect email or password", category="error")
                return redirect(url_for("login"))
        else:
            flash("Email not registered try to sign up", category="error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
