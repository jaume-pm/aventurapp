from controllers.user.homes import *
from controllers.user.inici import *
from controllers.user.subscripcions_ocasionals import *
from controllers.user.subscripcions_aventurers import *
from controllers.user.viatges import *

def routes_inici(app):
    app.route("/",methods=['GET', 'POST'])(inici)

def routes_homes(app):
    app.route("/log_in", methods=["GET", "POST"])(log_in)
    app.route("/sign_in", methods=["GET", "POST"])(sign_in)
    app.route("/canviar_contrassenya", methods=["GET", "POST"])(canviar_contrasenya)
    app.route("/home_ocasional", methods=["GET", "POST"])(home_ocasional)
    app.route("/home_aventurer", methods=["GET", "POST"])(home_aventurer)


def routes_inici_viatges(app):
    app.route("/home/viatges/crear", methods=["GET", "POST"])(home_viatges_crear)
    app.route("/home/viatges/llista", methods=["GET", "POST"])(home_viatges_llista)

def routes_inici_subscripcions_ocasionals(app):
    app.route("/home/aventurer/llista/crear", methods=["GET", "POST"])(home_aventurer_llista_crear)
    app.route("/home/aventurer/llista/modificar", methods=["GET", "POST"])(home_aventurer_llista_modificar)
    app.route("/home/aventurer/llista/seleccionar", methods=["GET", "POST"])(home_aventurer_llista_seleccionar)

def routes_inici_subscripcions_aventurers(app):
    app.route("/home/estatiques/subscriure", methods=["GET", "POST"])(home_estatiiques_subscriure)
    app.route("/home/subscripcions_estatiques", methods=["GET", "POST"])(home_subscripcions_estatiques)
    app.route("/home/subscripcions_estatiques", methods=["GET", "POST"])(home_subscripcions_estatiques)
    app.route("/home/subscripcions_aventurers_estatiques", methods=["GET", "POST"])(home_subscripcions_aventurers_estatiques)
    app.route("/home/personalitzades/subscriure", methods=["GET", "POST"])(home_personalitzades_subscriure)
    app.route("/home/subscripcions_aventurers_personalitzades", methods=["GET", "POST"])(home_subscripcions_aventurers_personalitzades)
