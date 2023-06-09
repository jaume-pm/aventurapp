from flask import Flask, request
from flask import render_template

#Private file which includes nom_usuari and password for my remote postgresql server 
from get_connection import get_db_connection;


app = Flask(__name__)



@app.route("/")
def inici():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.usuaris;')
    usuaris = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_usuaris_llista.html', usuaris=usuaris)






######################################################
# ADMINISTRACIÓ
######################################################

def rebre_info_usuari(nom_usuari):
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

def actualitzar_usuari(nom_usuari_objectiu, nom_usuari, nom, contrassenya):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE projecte.usuaris SET nom_usuari = %s, nom = %s, contrassenya = %s WHERE nom_usuari = %s"
    cur.execute(query, (nom_usuari, nom, contrassenya, nom_usuari_objectiu))
    conn.commit()
    cur.close()
    conn.close()

def crear_usuari(nom_usuari, nom, contrassenya):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya) VALUES (%s, %s, %s);"
    cur.execute(insert_query, (nom_usuari, nom, contrassenya))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_usuari(nom_usuari):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "DELETE FROM projecte.usuaris WHERE nom_usuari = %s;"
    cur.execute(insert_query, (nom_usuari,))
    conn.commit()
    cur.close()
    conn.close()

def crear_aventurer(nom_usuari):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "INSERT INTO projecte.aventurers (nom_usuari) VALUES (%s);"
    cur.execute(insert_query, (nom_usuari,))
    conn.commit()
    cur.close()
    conn.close()

def crear_ocasional(nom_usuari):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "INSERT INTO projecte.ocasionals (nom_usuari) VALUES (%s);"
    cur.execute(insert_query, (nom_usuari,))
    conn.commit()
    cur.close()
    conn.close()


@app.route('/admin/usuaris/modificar', methods=['GET', 'POST']) #TODO CANVIAR RUTA
def admin_usuaris_modificar():
    if request.method == 'POST':
        if 'rebre_valors' in request.form:
            nom_usuari_objectiu = request.form['nom_usuari_objectiu']
            nom, contrassenya = rebre_info_usuari(nom_usuari_objectiu)
            return render_template('admin_usuaris_modificar.html', nom_usuari_objectiu=nom_usuari_objectiu, nom_usuari=nom_usuari_objectiu, nom=nom, contrassenya=contrassenya)
        elif 'modificar' in request.form:
            nom_usuari_objectiu = request.form['nom_usuari_objectiu']
            nom_usuari = request.form['nom_usuari']
            nom = request.form['nom']
            contrassenya = request.form['contrassenya']
            actualitzar_usuari(nom_usuari_objectiu, nom_usuari, nom, contrassenya)
            return render_template('admin_usuaris_modificar.html', message="Dades de l'usuari " + nom_usuari_objectiu + " actualitzades.")
        
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

@app.route("/admin/aventurers/llista")
def admin_aventurers_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.aventurers;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_aventurers_llista.html', aventurers=aventurers)

@app.route("/admin/ocasionals/llista")
def admin_ocasionals_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.ocasionals;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_ocasionals_llista.html', aventurers=aventurers)



@app.route("/admin/usuaris/crear", methods=["GET", "POST"])
def admin_usuaris_crear():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        nom = request.form['nom']
        contrassenya = request.form['contrassenya']
        crear_usuari(nom_usuari, nom, contrassenya)
        aventurer = request.form.get('aventurer')
        if aventurer:
            crear_aventurer(nom_usuari)
        else:
            crear_ocasional(nom_usuari)
        return render_template('admin_usuaris_crear.html', message= "L'usuari " + nom_usuari + " s'ha creat correctament.")
    return render_template('admin_usuaris_crear.html')

@app.route("/admin/usuaris/eliminar", methods=["GET", "POST"])
def admin_usuaris_eliminar():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        eliminar_usuari(nom_usuari)
        return render_template('admin_usuaris_eliminar.html', message= "L'usuari " + nom_usuari + " s'ha eliminat correctament.")
    return render_template('admin_usuaris_eliminar.html')