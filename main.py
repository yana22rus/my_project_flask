from flask import Flask, render_template, request, flash
import sqlite3 as sq

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route("/")
def index():

    return render_template("index.htm")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.htm")

    lst = []

    if request.method == "POST":

        if request.form["registration"] == "Регистрация":

            with sq.connect("users.sql") as con:

                cur = con.cursor()

                cur.execute("SELECT login FROM users")

                for row in cur.fetchall():

                    if row[0] == request.form["login"]:

                        lst.append("Логин уже есть в системе")

                        break


            if request.form["login"] == request.form["password"]:

                lst.append("Логин не должен совпадать с паролем")

            if request.form["password"] != request.form["confirm_password"]:
                lst.append("Пароли должны совпадать")

            if len(request.form["password"]) < 8:
                lst.append(f'Длина пароля дожна быть более 8 символов вы ввели {len(request.form["password"])}')

            if len([x for x in list(request.form["password"]) if x.isupper()]) == 0:
                lst.append('Пароль должен содержать хотя бы одну прописную букву')

            if len([x for x in list(request.form["password"]) if x.isdigit()]) == 0:
                lst.append('Пароль должен содержать хотя бы одну цифру')


            if len(lst) == 0:

                query = "INSERT into users values (?,?,?,?);"

                with sq.connect("users.sql") as con:

                    cur = con.cursor()

                    cur.execute(
                        """ CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY NOT NULL,login TEXT,email TEXT,password TEXT)""")

                    cur.execute(query, (None, request.form["login"], request.form["email"], request.form["password"]))

                flash("все хорошо", category='success')


            else:

                [flash(x, category='error') for x in lst]

            return render_template("login.htm")

        del lst






if __name__ == "__main__":
    app.run(debug=True)