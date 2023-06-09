from flask import Flask, request, redirect
from flask import render_template

#Private file which includes nom_usuari and password for my remote postgresql server 
from get_connection import get_db_connection;


app = Flask(__name__)







######################################################
# ADMINISTRACIÓ
######################################################

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




##################################
# ADMINISTRACIÓ
##################################
@app.route("/admin")
def admin():
    classes = ["poblacions", "usuaris", "aventurers", "ocasionals", "viatges", "llistes"]
    return render_template('admin.html', classes=classes)


####################
# Usuaris
#####################

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


@app.route("/admin/usuaris/llista")
def admin_usuaris_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.usuaris ORDER BY nom_usuari;')
    usuaris = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_usuaris_llista.html', usuaris=usuaris)


####################
# Aventurers
####################

@app.route("/admin/aventurers/llista")
def admin_aventurers_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.aventurers ORDER BY nom_usuari;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_aventurers_llista.html', aventurers=aventurers)

@app.route("/admin/aventurers/crear")
def admin_aventurers_crear():
    return render_template('admin_aventurers_crear.html')


@app.route("/admin/aventurers/modificar")
def admin_aventurers_modificar():
    return render_template('admin_aventurers_modificar.html')

@app.route("/admin/aventurers/eliminar")
def admin_aventurers_eliminar():
    return render_template('admin_aventurers_eliminar.html')
####################
# Ocasionals
####################

@app.route("/admin/ocasionals/llista")
def admin_ocasionals_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.ocasionals ORDER BY nom_usuari;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_ocasionals_llista.html', aventurers=aventurers)

@app.route("/admin/ocasionals/eliminar")
def admin_ocasionals_eliminar():
    return render_template('admin_ocasionals_eliminar.html')

@app.route("/admin/ocasionals/crear")
def admin_ocasionals_crear():
    return render_template('admin_ocasionals_crear.html')

@app.route("/admin/ocasionals/modificar")
def admin_ocasionals_modificar():
    return render_template('admin_ocasionals_modificar.html')

####################################
## Poblacions
####################################

@app.route("/admin/poblacions/llista")
def admin_poblacions_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.poblacions ORDER BY nom_poblacio;')
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
        insert_query = "INSERT INTO projecte.poblacions (nom_poblacio, comarca, altitud, poblacio) VALUES (%s, %s, %s, %s);"
        cur.execute(insert_query, (nom, comarca, altitud, poblacio))
        conn.commit()
        cur.close()
        conn.close()
    return render_template('admin_poblacions_crear.html')

























##############################
## Aplicació Usuari
##############################

usuari_actiu = "2" #Variable global que indicarà l'usuari que ha iniciat sessió
es_aventurer = False

@app.route("/")
def inici():
    return render_template('inici.html')

# Retorna -1 si l'usuari no existeix, 0 si existeix però la contrassenya és incorrecta
# I 1 si l'usuari existeix i la contrassenya és correcte
def contrassenya_correcte(nom_usuari, contrassenya):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT contrassenya FROM projecte.usuaris WHERE nom_usuari = %s"
    cur.execute(query, (nom_usuari,))
    contrassenya_user = cur.fetchone()
    cur.close()
    conn.close()
    if contrassenya_user == None:
        return -1
    else:
        if contrassenya_user[0] == contrassenya:
            return 1
        else:
            return 0

def rebre_rol(nom_usuari):
    global es_aventurer
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT nom_usuari FROM projecte.aventurers WHERE nom_usuari = %s"
    cur.execute(query, (nom_usuari,))
    contrassenya_user = cur.fetchone()
    cur.close()
    conn.close()
    if contrassenya_user == None:
        es_aventurer = False
    else:
        es_aventurer = True

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    global usuari_actiu
    if request.method == 'POST':
        nom_usuari = request.form.get("nom_usuari")
        contrassenya = request.form.get("contrassenya")
        resultat = contrassenya_correcte(nom_usuari, contrassenya)
        if(resultat == 1):
            rebre_rol(nom_usuari)
            usuari_actiu = nom_usuari
            if(es_aventurer):
                return redirect("http://127.0.0.1:5000/home_aventurer")
            else:
                return redirect("http://127.0.0.1:5000/home_ocasional")
        elif(resultat == 0):
            return render_template('log_in.html', message="Contrassenya per a l'usuari " + nom_usuari + " incorrecta.")
        else:
            return render_template('log_in.html', message="L'usuari " + nom_usuari + " no existeix.")
    return render_template('log_in.html')

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
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
        return render_template('sign_in.html', message= "Benvingut a la familia Aventurapp " + nom_usuari + "!")
    return render_template('sign_in.html')


############
# Homes
############
@app.route("/home_ocasional")
def home_ocasional():
    return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)

@app.route("/home_aventurer")
def home_aventurer():
    return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)



############
# Viatges
############

@app.route("/home/viatges/crear", methods=["GET", "POST"])
def home_viatges_crear():
    if request.method == 'POST':
        if 'enviat' in request.form:
            nom_poblacio = request.form['nom_poblacio']
            conn = get_db_connection()
            cur = conn.cursor()
            insert_query = "INSERT INTO projecte.viatges (nom_poblacio, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (nom_poblacio,usuari_actiu))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_viatges_crear.html', message = "Viatge a " + nom_poblacio + " realitzat correctament.", usuari_actiu=usuari_actiu)
        elif 'tornar' in request.form:
            if es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)             
    return render_template('home_viatges_crear.html', usuari_actiu=usuari_actiu)

@app.route("/home/viatges/llista", methods=["GET", "POST"])
def home_viatges_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = 'SELECT * FROM projecte.viatges WHERE nom_usuari = %s ORDER BY nom_poblacio;'
    cur.execute(insert_query, (usuari_actiu))
    viatges = cur.fetchall()
    cur.close()
    conn.close()
    if request.method == 'POST':
            if es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
            
    return render_template('home_viatges_llista.html', viatges=viatges, usuari_actiu=usuari_actiu)

