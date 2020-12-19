from flask import request, jsonify, send_from_directory, redirect, url_for
import flask_login
from app import app, models


@app.route("/", methods=["GET"])
def get_autorization():
    print("/")
    print(flask_login.current_user.is_authenticated)
    if flask_login.current_user.is_authenticated:
        return redirect("/index")
    return app.send_static_file("autorize.html")


@app.route("/index.css", methods=["GET"])
def get_css():
    return app.send_static_file("index.css")


@app.route("/reg", methods=["GET"])
def get_reg():
    print("reg")
    print(flask_login.current_user.is_authenticated)
    if flask_login.current_user.is_authenticated:
        return redirect("/index")
    return app.send_static_file("reg.html")


@app.route("/index", methods=["GET"])
def get_index():
    print("index")
    print(flask_login.current_user.is_authenticated)
    if not flask_login.current_user.is_authenticated:
        return redirect("/")
    with open ("app/static/index.html", 'r', encoding='utf-8') as f:
        text = f.read()
        print(text)
        reg = "Имя"
        login = flask_login.current_user.login
        text = text.replace(reg, login)
        print(text)

    with open ("app/static/index_correct.html", 'w', encoding='utf-8') as f:
        f.write(text)
    return app.send_static_file("index_correct.html")


@app.route("/about", methods=["GET"])
def get_about():
    if not flask_login.current_user.is_authenticated:
        return redirect("/")
    return app.send_static_file("about.html")


@app.route("/img/<name>", methods=["GET"])
def get_cat(name):
    print(app.config["IMG_DIR"])
    return send_from_directory(
        app.config["IMG_DIR"], name, as_attachment=True)


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if models.User.query.filter_by(login=data['login']).first() \
            is not None:
        return jsonify({'status': -1})
    models.User.registrate(data["login"], data["password"])
    return jsonify({"status": 0})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = models.User.query.filter_by(login=data['login']).first()
    if user is None or not user.check_password(data["password"]):
        return jsonify({'status': -1})
    flask_login.login_user(user)
    return jsonify({'status': 0})


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
