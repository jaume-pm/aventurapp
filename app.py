from flask import Flask, request
from flask import render_template

#Private file which includes nom_usuari and password for my remote postgresql server 
from get_connection import get_db_connection;


app = Flask(__name__)

def get_user_info(nom_usuari):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT nom, contrassenya FROM projecte.usuaris WHERE nom_usuari = %s"
    cur.execute(query, (nom_usuari,))
    info = cur.fetchone()
    nom = info[0]
    contrassenya = info[1]
    cur.close()
    conn.close()
    return nom, contrassenya

@app.route('/', methods=['GET', 'POST']) #TODO CANVIAR RUTA
def admin_usuaris_modificar():
    if request.method == 'POST':
        if 'rebre_valors' in request.form:
            nom_usuari = request.form['nom_usuari']
            print("a")
            nom, contrassenya = get_user_info(nom_usuari)
            return render_template('admin_usuaris_modificar.html', nom_usuari=nom_usuari, nom=nom, contrassenya=contrassenya)
        elif 'modificar' in request.form:
            nom_usuari = request.form['nom_usuari']
            nom = request.form['nom']
            contrassenya = request.form['modificar']
            #update_user_password(nom_usuari, modified_password)
            return render_template('admin_usuaris_modificar.html', message='Password updated successfully!')
        
    return render_template('admin_usuaris_modificar.html')



@app.route("/admin")
def admin():
    classes = ["poblacions", "usuaris", "aventurers", "ocasionals", "viatges", "llistes"]
    return render_template('admin.html', classes=classes)


@app.route("/admin/poblacions/llista")
def admin_poblacions_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.poblacions;')
    poblacions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_poblacions_llista.html', poblacions=poblacions)

@app.route("/admin/poblacions/crear", methods=["GET", "POST"])
def admin_poblacions_crear():
    if request.method == 'POST':
        nom = request.form['nom_poblacio']
        comarca = request.form['comarca']
        altitud = request.form['altitud']
        poblacio = request.form['poblacio']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "INSERT INTO projecte.poblacions (nom, comarca, altitud, poblacio) VALUES (%s, %s, %s, %s);"
        cur.execute(insert_query, (nom, comarca, altitud, poblacio))
        conn.commit()
        cur.close()
        conn.close()
    return render_template('admin_poblacions_crear.html')

@app.route("/admin/usuaris/llista")
def admin_usuaris_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.usuaris;')
    usuaris = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_usuaris_llista.html', usuaris=usuaris)

@app.route("/admin/aventurers")
def admin_aventurers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.aventurers;')
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