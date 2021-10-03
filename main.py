from flask import Flask,render_template,request


app = Flask(__name__)

@app.route("/")
def index():

    return "hello world"


@app.route("/login",methods=["POST","GET"])
def login():

    return render_template("login.htm")


if __name__ == "__main__":

    app.run(debug=True)