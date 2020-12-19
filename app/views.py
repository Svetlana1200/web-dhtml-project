from flask import request, jsonify, send_from_directory, redirect
import flask_login
from app import app, models


@app.route("/", methods=["GET"])
def get_autorization():
    print(flask_login.current_user.is_authenticated)
    if flask_login.current_user.is_authenticated:
        return redirect("/index")
    return app.send_static_file("autorize.html")


@app.route("/index.css", methods=["GET"])
def get_css():
    return app.send_static_file("index.css")


@app.route("/reg", methods=["GET"])
def get_reg():
    print(flask_login.current_user.is_authenticated)

    if flask_login.current_user.is_authenticated:
        return redirect("/index")
    return app.send_static_file("reg.html")


@app.route("/index", methods=["GET"])
def get_index():
    if not flask_login.current_user.is_authenticated:
        return redirect("/")
    return app.send_static_file("index.html")


@app.route("/about", methods=["GET"])
def get_about():
    if not flask_login.current_user.is_authenticated:
        return redirect("/")
    return app.send_static_file("about.html")


@app.route("/cats/<name>", methods=["GET"])
def get_cat(name):
    print(app.config["CATS_DIR"])
    return send_from_directory(
        app.config["CATS_DIR"], name, as_attachment=True)


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
