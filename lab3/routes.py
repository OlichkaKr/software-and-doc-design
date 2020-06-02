from flask import jsonify, render_template, request, abort, Blueprint, redirect, url_for, send_from_directory, Response
from api import UserModelView
from models import User

base_bp = Blueprint('base', __name__)

user = UserModelView()


@base_bp.route("/", methods=["GET"])
def redirect():
    return render_template("get.html")


@base_bp.route("/user", methods=["GET"])
def redirect_to():
    return render_template("get.html")


@base_bp.route("/user/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('create.html')
    elif request.method == "POST":
        user.post(request.values)
        return redirect()
    else:
        return abort(404)


@base_bp.route("/user/edit/<obj_id>", methods=["GET", "PUT"])
def user_edit(obj_id):
    if request.method == "GET":
        return render_template('edit.html', obj_id=obj_id)
    elif request.method == "PUT":
        print(request.values)
        user.update(obj_id, request.values)
        print('redirect')
        return Response("updated", 200)
    else:
        return abort(404)
    print('redirect2')
    return redirect()


@base_bp.route("/user/delete/<obj_id>", methods=["DELETE"])
def user_delete(obj_id):
    return user.delete(obj_id)