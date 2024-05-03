from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def signup():
    return render_template("signup.html")




app.run(debug=True, port=5001)