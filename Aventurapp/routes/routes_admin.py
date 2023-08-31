from controllers.admin.aventurers import *
from controllers.admin.continguts import *
from controllers.admin.estatiques import *
from controllers.admin.home import *
from controllers.admin.llistes import *
from controllers.admin.ocasionals import *
from controllers.admin.personalitzades import *
from controllers.admin.poblacions import *
from controllers.admin.subscripcions_aventurers import *
from controllers.admin.subscripcions_ocasionals import *
from controllers.admin.usuaris import *
from controllers.admin.viatges import *


def routes_users(app):
    app.route('/admin/usuaris/modificar', methods=['GET', 'POST'])(admin_usuaris_modificar)
    app.route("/admin/usuaris/crear", methods=["GET", "POST"])(admin_usuaris_crear)
    app.route("/admin/usuaris/eliminar", methods=["GET", "POST"])(admin_usuaris_eliminar)
    app.route("/admin/usuaris/llista", methods=["GET", "POST"])(admin_usuaris_llista)

def routes_aventurers(app):
    app.route("/admin/aventurers/llista", methods=["GET", "POST"])(admin_aventurers_llista)
    app.route("/admin/aventurers/crear", methods=["GET", "POST"])(admin_aventurers_crear)
    app.route("/admin/aventurers/modificar", methods=["GET", "POST"])(admin_aventurers_modificar)
    app.route("/admin/aventurers/eliminar", methods=["GET", "POST"])(admin_aventurers_eliminar)

def routes_home(app):
    app.route("/admin")(admin)

def routes_ocasionals(app):
    app.route("/admin/ocasionals/llista", methods=["GET", "POST"])(admin_ocasionals_llista)
    app.route("/admin/ocasionals/eliminar", methods=["GET", "POST"])(admin_ocasionals_eliminar)
    app.route("/admin/ocasionals/crear", methods=["GET", "POST"])(admin_ocasionals_crear)
    app.route("/admin/ocasionals/modificar", methods=["GET", "POST"])(admin_ocasionals_modificar)

def routes_poblacions(app):
    app.route("/admin/poblacions/llista", methods=["GET", "POST"])(admin_poblacions_llista)
    app.route("/admin/poblacions/eliminar", methods=["GET", "POST"])(admin_poblacions_eliminar)
    app.route("/admin/poblacions/crear", methods=["GET", "POST"])(admin_poblacions_crear)
    app.route("/admin/poblacions/modificar", methods=["GET", "POST"])(admin_poblacions_modificar)

def routes_viatges(app):
    app.route("/admin/viatges/llista", methods=["GET", "POST"])(admin_viatges_llista)
    app.route("/admin/viatges/eliminar", methods=["GET", "POST"])(admin_viatges_eliminar)
    app.route("/admin/viatges/crear", methods=["GET", "POST"])(admin_viatges_crear)
    app.route("/admin/viatges/modificar", methods=["GET", "POST"])(admin_viatges_modificar)

def routes_llistes(app):
    app.route("/admin/llistes/llista", methods=["GET", "POST"])(admin_llistes_llista)
    app.route("/admin/llistes/eliminar", methods=["GET", "POST"])(admin_llistes_eliminar)
    app.route("/admin/llistes/crear", methods=["GET", "POST"])(admin_llistes_crear)
    app.route("/admin/llistes/modificar", methods=["GET", "POST"])(admin_llistes_modificar)

def routes_estatiques(app):
    app.route("/admin/estatiques/llista", methods=["GET", "POST"])(admin_estatiques_llista)
    app.route("/admin/estatiques/eliminar", methods=["GET", "POST"])(admin_estatiques_eliminar)
    app.route("/admin/estatiques/crear", methods=["GET", "POST"])(admin_estatiques_crear)
    app.route("/admin/estatiques/modificar", methods=["GET", "POST"])(admin_estatiques_modificar)

def routes_personalitzades(app):
    app.route("/admin/personalitzades/llista", methods=["GET", "POST"])(admin_personalitzades_llista)
    app.route("/admin/personalitzades/eliminar", methods=["GET", "POST"])(admin_personalitzades_eliminar)
    app.route("/admin/personalitzades/crear", methods=["GET", "POST"])(admin_personalitzades_crear)
    app.route("/admin/personalitzades/modificar", methods=["GET", "POST"])(admin_personalitzades_modificar)

def routes_continguts(app):
    app.route("/admin/continguts/llista", methods=["GET", "POST"])(admin_continguts_llista)
    app.route("/admin/continguts/eliminar", methods=["GET", "POST"])(admin_continguts_eliminar)
    app.route("/admin/continguts/crear", methods=["GET", "POST"])(admin_continguts_crear)
    app.route("/admin/continguts/modificar", methods=["GET", "POST"])(admin_continguts_modificar)

def routes_subscripcions_aventurers(app):
    app.route("/admin/subscripcions_aventurers/llista", methods=["GET", "POST"])(admin_subscripcions_aventurers_llista)
    app.route("/admin/subscripcions_aventurers/eliminar", methods=["GET", "POST"])(admin_subscripcions_aventurers_eliminar)
    app.route("/admin/subscripcions_aventurers/crear", methods=["GET", "POST"])(admin_subscripcions_aventurers_crear)
    app.route("/admin/subscripcions_aventurers/modificar", methods=["GET", "POST"])(admin_subscripcions_aventurers_modificar)

def routes_subscripcions_ocasionals(app):
    app.route("/admin/subscripcions_ocasionals/llista", methods=["GET", "POST"])(admin_subscripcions_ocasionals_llista)
    app.route("/admin/subscripcions_ocasionals/eliminar", methods=["GET", "POST"])(admin_subscripcions_ocasionals_eliminar)
    app.route("/admin/subscripcions_ocasionals/crear", methods=["GET", "POST"])(admin_subscripcions_ocasionals_crear)
    app.route("/admin/subscripcions_ocasionals/modificar", methods=["GET", "POST"])(admin_subscripcions_ocasionals_modificar)

