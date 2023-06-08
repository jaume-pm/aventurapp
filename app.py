from flask import Flask, request
from flask import render_template

#Private file which includes username and password for my remote postgresql server 
from get_connection import get_db_connection;


app = Flask(__name__)


@app.route("/admin")
def admin():
    classes = ["poblacions", "usuaris", "aventurers", "ocasionals", "viatges", "llistes"]
    return render_template('admin.html', classes=classes)


@app.route("/admin/poblacions/llista")
def admin_poblacions_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM practica.poblacions;')
    poblacions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_poblacions.html', poblacions=poblacions)

@app.route("/admin/aventurers")
def admin_aventurers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM practica.aventurers;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_aventurers.html', aventurers=aventurers)

@app.route("/admin/usuaris")
def admin_usuaris():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.usuaris;')
    usuaris = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_usuaris.html', usuaris=usuaris)

@app.route("/admin/usuaris/crear", methods=["GET", "POST"])
def admin_usuaris_crear():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        nom = request.form['nom']
        contrassenya = request.form['contrassenya']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya) VALUES (%s, %s, %s);"
        cur.execute(insert_query, (nom_usuari, nom, contrassenya))
        conn.commit()
        cur.close()
        conn.close()
    return render_template('admin_usuaris_crear.html')