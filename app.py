from flask import Flask, request, redirect
from flask import render_template

#Private file which includes nom_usuari and password for my remote postgresql server 
from get_connection import get_db_connection;
import psycopg2

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
    classes = ["poblacions", "usuaris", "aventurers", "ocasionals", "viatges", "llistes",
               "estatiques", "personalitzades", "continguts", "subscripcions_aventurers",
               "subscripcions_ocasionals"]
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

def rebre_info_poblacio(nom_poblacio_objectiu):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT comarca, altitud, poblacio FROM projecte.poblacions WHERE nom_poblacio = %s"
    cur.execute(query, (nom_poblacio_objectiu,))
    info = cur.fetchone()
    comarca = info[0]
    altitud = info[1]
    poblacio = info[2]
    cur.close()
    conn.close()
    return comarca, altitud, poblacio

def actualitzar_poblacio(nom_poblacio_objectiu, nom_poblacio, comarca, altitud, poblacio):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE projecte.poblacions SET nom_poblacio = %s, comarca = %s, altitud = %s, poblacio = %s WHERE nom_poblacio = %s"
    cur.execute(query, (nom_poblacio, comarca, altitud, poblacio, nom_poblacio_objectiu))
    conn.commit()
    cur.close()
    conn.close()


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
        return render_template('admin_poblacions_crear.html', message= "S'ha afegit la població " 
                           + nom + " al sistema. ")
    return render_template('admin_poblacions_crear.html')

@app.route('/admin/poblacions/modificar', methods=['GET', 'POST']) #TODO CANVIAR RUTA
def admin_poblacions_modificar():
    if request.method == 'POST':
        if 'rebre_valors' in request.form:
            nom_poblacio_objectiu = request.form['nom_poblacio_objectiu']
            comarca, altitud, poblacio = rebre_info_poblacio(nom_poblacio_objectiu)
            return render_template('admin_poblacions_modificar.html', nom_poblacio_objectiu=nom_poblacio_objectiu, nom_poblacio=nom_poblacio_objectiu,
                                   altitud=altitud, comarca=comarca, poblacio=poblacio)
        elif 'modificar' in request.form:
            nom_poblacio_objectiu = request.form['nom_poblacio_objectiu']
            nom_poblacio = request.form['nom_poblacio']
            comarca = request.form['comarca']
            altitud = request.form['altitud']
            poblacio = request.form['poblacio']
            actualitzar_poblacio(nom_poblacio_objectiu, nom_poblacio, comarca, altitud, poblacio)
            return render_template('admin_poblacions_modificar.html',
                                   message="Dades de la població " + nom_poblacio + " actualitzades.")
        
    return render_template('admin_poblacions_modificar.html')


@app.route("/admin/poblacions/eliminar", methods=['GET', 'POST'])
def admin_poblacions_eliminar():
    if request.method == 'POST':
        nom_poblacio = request.form['nom_poblacio']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.poblacions WHERE nom_poblacio = %s;"
        cur.execute(insert_query, (nom_poblacio,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_poblacions_eliminar.html', message= "S'ha eliminat la població: " 
                               + nom_poblacio)
    return render_template('admin_poblacions_eliminar.html')

############
# Viatges
############



@app.route("/admin/viatges/crear", methods=["GET", "POST"])
def admin_viatges_crear():
    if request.method == 'POST':
        if 'enviat' in request.form:
            nom_usuari = request.form['nom_usuari']
            nom_poblacio = request.form['nom_poblacio']
            conn = get_db_connection()
            cur = conn.cursor()
            insert_query = "INSERT INTO projecte.viatges (nom_poblacio, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (nom_poblacio,nom_usuari))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('admin_viatges_crear.html', message = "Viatge a " + nom_poblacio + " realitzat per l'usuari "
                                   + nom_usuari +" realitzar correctament.")
        
    return render_template('admin_viatges_crear.html')

@app.route("/admin/viatges/llista", methods=["GET", "POST"])
def admin_viatges_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = 'SELECT * FROM projecte.viatges WHERE nom_usuari = %s ORDER BY nom_poblacio;'
    cur.execute(insert_query, (usuari_actiu))
    viatges = cur.fetchall()
    cur.close()
    conn.close()
    if request.method == 'POST':
            if es_aventurer:
                return render_template('admin_aventurer.html', usuari_actiu=usuari_actiu)
            else:
                return render_template('admin_ocasional.html', usuari_actiu=usuari_actiu)
            
    return render_template('admin_viatges_llista.html', viatges=viatges, usuari_actiu=usuari_actiu)


@app.route("/admin/viatges/eliminar", methods=['GET', 'POST'])
def admin_viatges_eliminar():
    if request.method == 'POST':
        codi_viatge = request.form['codi_viatge']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.viatges WHERE id_viatge = %s;"
        cur.execute(insert_query, (codi_viatge,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_viatges_eliminar.html', message= "S'ha eliminat el viatge amb codi: " 
                               + str(codi_viatge))
    return render_template('admin_viatges_eliminar.html')


@app.route("/admin/viatges/modificar")
def admin_viatges_modificar():
    return render_template('admin_viatges_modificar.html')

#######################
# Llistes
#######################


def crear_llista(titol):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "INSERT INTO projecte.llistes (titol) VALUES (%s);"
    cur.execute(insert_query, (titol,))
    conn.commit()
    insert_query = "SELECT codi_llista FROM projecte.llistes WHERE titol = %s;"
    cur.execute(insert_query, (titol,))
    conn.commit()
    codi_llista = cur.fetchall()[0][0]
    print(codi_llista)
    cur.close()
    conn.close()
    return int(codi_llista)

def crear_estatica(codi_llista):
    conn = get_db_connection()
    cur = conn.cursor()
    print(codi_llista)
    insert_query = "INSERT INTO projecte.estatiques (codi_llista) VALUES (%s);"
    cur.execute(insert_query, (codi_llista,))
    conn.commit()
    cur.close()
    conn.close()

def crear_personalitzada(codi_llista, creador):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "INSERT INTO projecte.personalitzades (codi_llista, nom_usuari) VALUES (%s, %s);"
    cur.execute(insert_query, (codi_llista, creador,))
    conn.commit()
    cur.close()
    conn.close()

def rebre_info_llista_titol(codi_llista_objectiu):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "SELECT titol from projecte.llistes WHERE codi_llista = %s;"
    cur.execute(insert_query, (codi_llista_objectiu,))
    titol = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return titol

def es_personalitzada(codi_llista_objectiu):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "SELECT codi_llista from projecte.personalitzades WHERE codi_llista = %s;"
    cur.execute(insert_query, (codi_llista_objectiu,))
    es_personalitzada = cur.fetchone()
    cur.close()
    conn.close()
    if es_personalitzada == None:
        return False
    else:
        return True
    
def rebre_info_llista_creador(codi_llista_objectiu):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "SELECT nom_usuari from projecte.personalitzades WHERE codi_llista = %s;"
    cur.execute(insert_query, (codi_llista_objectiu,))
    creador = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return creador

def actualitzar_personalitzada(codi_llista_objectiu, codi_llista, titol, creador):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE projecte.llistes SET codi_llista = %s, titol = %s WHERE codi_llista = %s"
    cur.execute(query, (codi_llista, titol, codi_llista_objectiu))
    conn.commit()
    query = "UPDATE projecte.personalitzades SET nom_usuari = %s WHERE codi_llista = %s"
    cur.execute(query, (creador, codi_llista))
    conn.commit()
    cur.close()
    conn.close()

def actualitzar_estatica(codi_llista_objectiu, codi_llista, titol):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE projecte.llistes SET codi_llista = %s, titol = %s WHERE codi_llista = %s"
    cur.execute(query, (codi_llista, titol, codi_llista_objectiu))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_llista(codi_llista):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = "DELETE FROM projecte.llistes WHERE codi_llista = %s;"
    cur.execute(insert_query, (codi_llista,))
    conn.commit()
    cur.close()
    conn.close()

@app.route("/admin/llistes/crear", methods=["GET", "POST"])
def admin_llistes_crear():
    if request.method == 'POST':
        titol = request.form['titol']
        codi_llista = crear_llista(titol)
        es_personalitzada = request.form.get('personalitzada')
        if es_personalitzada:
            creador = request.form['creador']
            crear_personalitzada(codi_llista, creador)
        else:
            crear_estatica(codi_llista)
        return render_template('admin_llistes_crear.html', message= "La llista" + titol + " amb codi = " + str(codi_llista) +  " s'ha creat correctament.")
    return render_template('admin_llistes_crear.html')

@app.route("/admin/llistes/llista")
def admin_llistes_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.llistes ORDER BY codi_llista;')
    llistes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_llistes_llista.html', llistes=llistes)


personalitzada = False #global variable per no haver de comprovar 2 vegades
                        #si la llista es estatica
@app.route('/admin/llistes/modificar', methods=['GET', 'POST'])
def admin_llistes_modificar():
    global personalitzada
    if request.method == 'POST':
        if 'rebre_valors' in request.form:
            codi_llista_objectiu = request.form['codi_llista_objectiu']
            titol = rebre_info_llista_titol(codi_llista_objectiu)
            personalitzada = es_personalitzada(codi_llista_objectiu)
            if personalitzada:
                creador = rebre_info_llista_creador(codi_llista_objectiu)
                return render_template('admin_llistes_modificar.html', codi_llista_objectiu=codi_llista_objectiu, 
                                       codi_llista=codi_llista_objectiu, titol=titol, creador=creador)
            else:
                return render_template('admin_llistes_modificar.html', codi_llista_objectiu=codi_llista_objectiu,
                                        codi_llista=codi_llista_objectiu, titol=titol)
        elif 'modificar' in request.form:
            codi_llista_objectiu = request.form['codi_llista_objectiu']
            codi_llista = request.form['codi_llista']
            titol = request.form['titol']
            if personalitzada:
                creador = request.form['creador']
                actualitzar_personalitzada(codi_llista_objectiu, codi_llista, titol, creador)
            else:
                actualitzar_estatica(codi_llista_objectiu, codi_llista, titol)
            return render_template('admin_llistes_modificar.html', message="Dades de la llista " + str(codi_llista) + " amb títol " + titol + " actualitzades.")
        
    return render_template('admin_llistes_modificar.html')

@app.route("/admin/llistes/eliminar", methods=['GET', 'POST'])
def admin_llistes_eliminar():
    if request.method == 'POST':
        codi_llista = request.form['codi_llista']
        eliminar_llista(codi_llista)
        return render_template('admin_llistes_eliminar.html', message= "La llista " + codi_llista + " s'ha eliminat correctament.")
    return render_template('admin_llistes_eliminar.html')


###############################
# Estatiques
###############################

@app.route("/admin/estatiques/llista")
def admin_estatiques_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.estatiques ORDER BY codi_llista;')
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_estatiques_llista.html', estatiques=estatiques)

@app.route("/admin/estatiques/eliminar")
def admin_estatiques_eliminar():
    return render_template('admin_estatiques_eliminar.html')

@app.route("/admin/estatiques/crear")
def admin_estatiques_crear():
    return render_template('admin_estatiques_crear.html')

@app.route("/admin/estatiques/modificar")
def admin_estatiques_modificar():
    return render_template('admin_estatiques_modificar.html')

###############################
# Personalitzades
###############################

@app.route("/admin/personalitzades/llista")
def admin_personalitzades_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.personalitzades ORDER BY codi_llista;')
    personalitzades = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_personalitzades_llista.html', personalitzades=personalitzades)

@app.route("/admin/personalitzades/eliminar")
def admin_personalitzades_eliminar():
    return render_template('admin_personalitzades_eliminar.html')

@app.route("/admin/personalitzades/crear")
def admin_personalitzades_crear():
    return render_template('admin_personalitzades_crear.html')

@app.route("/admin/personalitzades/modificar")
def admin_personalitzades_modificar():
    return render_template('admin_personalitzades_modificar.html')

##############################
## Continguts
##############################


@app.route("/admin/continguts/llista")
def admin_continguts_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.continguts ORDER BY codi_llista;')
    continguts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_continguts_llista.html', continguts=continguts)


@app.route("/admin/continguts/crear", methods=["GET", "POST"])
def admin_continguts_crear():
    if request.method == 'POST':
        nom_poblacio = request.form['nom_poblacio']
        codi_llista = request.form['codi_llista']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "INSERT INTO projecte.continguts (nom_poblacio, codi_llista) VALUES (%s, %s);"
        cur.execute(insert_query, (nom_poblacio, codi_llista))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_continguts_crear.html', message= "S'ha afegit la població " 
                           + nom_poblacio + " a la llista amb codi " + str(codi_llista))
    return render_template('admin_continguts_crear.html')



@app.route("/admin/continguts/modificar")
def admin_continguts_modificar():
    return render_template('admin_continguts_modificar.html')


##############################
## Subscripcions_aventurers
##############################

@app.route("/admin/subscripcions_aventurers/llista")
def admin_subscripcions_aventurers_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.subscripcions_aventurers ORDER BY nom_usuari;')
    continguts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_subscripcions_aventurers_llista.html', continguts=continguts)

@app.route("/admin/subscripcions_aventurers/crear", methods=["GET", "POST"])
def admin_subscripcions_aventurers_crear():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        codi_llista = request.form['codi_llista']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "INSERT INTO projecte.subscripcions_aventurers (nom_usuari, codi_llista) VALUES (%s, %s);"
        cur.execute(insert_query, (nom_usuari, codi_llista))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_subscripcions_aventurers_crear.html', message= "L'usuari "
                           + nom_usuari + " s'ha subscrit a la llista amb codi " + str(codi_llista))
    return render_template('admin_subscripcions_aventurers_crear.html')

@app.route("/admin/subscripcions_aventurers/eliminar", methods=['GET', 'POST'])
def admin_subscripcions_aventurers_eliminar():
    if request.method == 'POST':
        codi_llista = request.form['codi_llista']
        nom_usuari = request.form['nom_usuari']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_aventurers WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, nom_usuari,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_subscripcions_aventurers_eliminar.html', message= "S'ha eliminat la subscripció de l'aventurer " 
                           + nom_usuari + " a la llista amb codi " + str(codi_llista))
    return render_template('admin_subscripcions_aventurers_eliminar.html')

@app.route("/admin/subscripcions_aventurers/modificar")
def admin_subscripcions_aventurers_modificar():
    return render_template('admin_subscripcions_aventurers_modificar.html')


###########################
# Subscripcions_ocasionals
############################

@app.route("/admin/subscripcions_ocasionals/llista")
def admin_subscripcions_ocasionals_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.subscripcions_ocasionals ORDER BY nom_usuari;')
    continguts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_subscripcions_ocasionals_llista.html', continguts=continguts)

@app.route("/admin/subscripcions_ocasionals/crear", methods=["GET", "POST"])
def admin_subscripcions_ocasionals_crear():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        codi_llista = request.form['codi_llista']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "INSERT INTO projecte.subscripcions_ocasionals (nom_usuari, codi_llista) VALUES (%s, %s);"
        cur.execute(insert_query, (nom_usuari, codi_llista))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_subscripcions_ocasionals_crear.html', message= "L'usuari "
                           + nom_usuari + " s'ha subscrit a la llista amb codi " + str(codi_llista))
    return render_template('admin_subscripcions_ocasionals_crear.html')

@app.route("/admin/subscripcions_ocasionals/eliminar", methods=['GET', 'POST'])
def admin_subscripcions_ocasionals_eliminar():
    if request.method == 'POST':
        codi_llista = request.form['codi_llista']
        nom_usuari = request.form['nom_usuari']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_ocasionals WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, nom_usuari,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_subscripcions_ocasionals_eliminar.html', message= "S'ha eliminat la subscripció de l'ocasional " 
                           + nom_usuari + " a la llista amb codi " + str(codi_llista))
    return render_template('admin_subscripcions_ocasionals_eliminar.html')

@app.route("/admin/subscripcions_ocasionals/modificar")
def admin_subscripcions_ocasionals_modificar():
    return render_template('admin_subscripcions_ocasionals_modificar.html')



##############################
## Aplicació Usuari
##############################

usuari_actiu = "2" #Variable global que indicarà l'usuari que ha iniciat sessió
es_aventurer = True

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
    insert_query = 'SELECT nom_poblacio FROM projecte.viatges WHERE nom_usuari = %s ORDER BY nom_poblacio;'
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


############################
# Estatiques i subscripcions ocasionals
############################

@app.route("/home/estatiques/subscriure", methods=["GET", "POST"])
def home_estatiiques_subscriure():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = ("SELECT l.titol, l.codi_llista, array_agg(c.nom_poblacio) " +
                    "FROM projecte.estatiques AS e " +
                    "JOIN projecte.llistes AS l ON e.codi_llista = l.codi_llista " +
                    "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista " +
                    "GROUP BY l.titol, l.codi_llista;")
    cur.execute(insert_query)
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    print("entramo")
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if es_aventurer:
                insert_query = "INSERT INTO projecte.subscripcions_aventurers (codi_llista, nom_usuari) VALUES (%s, %s);"
            else:
                insert_query = "INSERT INTO projecte.subscripcions_ocasionals (codi_llista, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, usuari_actiu,))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_estatiques_subscriure.html', message="T'has subscrit a la llista " + titol,
                                   usuari_actiu=usuari_actiu, estatiques=estatiques)
        except psycopg2.errors.UniqueViolation:
            message = "Ja estas subscrit a aquesta llista, només et pots subscriure una vegada a cada llista."
            return render_template('home_estatiques_subscriure.html', message=message,
                                   estatiques=estatiques, usuari_actiu=usuari_actiu)
    elif 'tornar' in request.form:
        if es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
    return render_template('home_estatiques_subscriure.html', estatiques=estatiques, usuari_actiu=usuari_actiu)

def rebre_subscripcions_ocasionals():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol, l.codi_llista, array_agg(c.nom_poblacio) "
        "FROM projecte.subscripcions_ocasionals AS s "
        "JOIN projecte.llistes AS l ON s.codi_llista = l.codi_llista "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "WHERE s.codi_llista IN ("
        "   SELECT codi_llista "
        "   FROM projecte.subscripcions_aventurers "
        "   WHERE nom_usuari = %s"
        ") "
        "GROUP BY l.titol, l.codi_llista"
    )
    cur.execute(insert_query, (usuari_actiu,))
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    return estatiques

def rebre_subscripcions_aventurers_estatiques():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol, l.codi_llista, array_agg(c.nom_poblacio) "
        "FROM projecte.llistes AS l "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "WHERE l.codi_llista IN ("
        "    SELECT sa.codi_llista "
        "    FROM projecte.subscripcions_aventurers AS sa "
        "    WHERE sa.nom_usuari = %s"
        ") "
        "AND l.codi_llista IN ("
        "    SELECT e.codi_llista "
        "    FROM projecte.estatiques AS e"
        ") "
        "GROUP BY l.titol, l.codi_llista"
    )
    cur.execute(insert_query, (usuari_actiu,))
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    return estatiques

@app.route("/home/subscripcions_estatiques", methods=["GET", "POST"])
def home_subscripcions_estatiques():
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_ocasionals WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        estatiques = rebre_subscripcions_ocasionals()
        return render_template('home_subscripcions_estatiques.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=usuari_actiu, estatiques=estatiques)
    elif 'tornar' in request.form:
        if es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
    estatiques = rebre_subscripcions_ocasionals()
    return render_template('home_subscripcions_estatiques.html', estatiques=estatiques, usuari_actiu=usuari_actiu)

@app.route("/home/subscripcions_aventurers_estatiques", methods=["GET", "POST"])
def home_subscripcions_aventurers_estatiques():
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_aventurers WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        estatiques = rebre_subscripcions_aventurers_estatiques()
        return render_template('home_subscripcions_aventurers_estatiques.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=usuari_actiu, estatiques=estatiques)
    elif 'tornar' in request.form:
        if es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
    estatiques = rebre_subscripcions_aventurers_estatiques()
    return render_template('home_subscripcions_aventurers_estatiques.html', estatiques=estatiques, usuari_actiu=usuari_actiu)


def rebre_subscripcions_personalitzades():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol, l.codi_llista, p.nom_usuari, array_agg(c.nom_poblacio) "
        "FROM projecte.llistes AS l "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "JOIN projecte.personalitzades AS p ON l.codi_llista = p.codi_llista "
        "WHERE l.codi_llista IN ("
        "    SELECT sa.codi_llista "
        "    FROM projecte.subscripcions_aventurers AS sa "
        "    WHERE sa.nom_usuari = %s"
        ") "
        "AND l.codi_llista NOT IN (" #Hi ha menys estàtiques. Millor mirar si no es estática.
        "    SELECT e.codi_llista "
        "    FROM projecte.estatiques AS e"
        ") "
        "GROUP BY l.titol, l.codi_llista, p.nom_usuari"
    )
    cur.execute(insert_query, (usuari_actiu,))
    personalitzades = cur.fetchall()
    cur.close()
    conn.close()
    return personalitzades

def rebre_personalitzades():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol, l.codi_llista, p.nom_usuari, array_agg(c.nom_poblacio) "
        "FROM projecte.llistes AS l "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "JOIN projecte.personalitzades AS p ON l.codi_llista = p.codi_llista "
        "WHERE l.codi_llista NOT IN (" #Hi ha menys estàtiques. Millor mirar si no es estática.
        "    SELECT e.codi_llista "
        "    FROM projecte.estatiques AS e"
        ") "
        "GROUP BY l.titol, l.codi_llista, p.nom_usuari"
    )
    cur.execute(insert_query)
    personalitzades = cur.fetchall()
    cur.close()
    conn.close()
    return personalitzades

@app.route("/home/personalitzades/subscriure", methods=["GET", "POST"])
def home_personalitzades_subscriure():
    if 'codi_llista' in request.form:
        personalitzades = rebre_personalitzades()
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if es_aventurer:
                insert_query = "INSERT INTO projecte.subscripcions_aventurers (codi_llista, nom_usuari) VALUES (%s, %s);"
            else:
                insert_query = "INSERT INTO projecte.subscripcions_ocasionals (codi_llista, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, usuari_actiu,))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_personalitzades_subscriure.html', message="T'has subscrit a la llista " + titol,
                                   usuari_actiu=usuari_actiu, personalitzades=personalitzades)
        except psycopg2.errors.UniqueViolation:
            message = "Ja estas subscrit a aquesta llista, només et pots subscriure una vegada a cada llista."
            return render_template('home_personalitzades_subscriure.html', message=message,
                                   personalitzades=personalitzades, usuari_actiu=usuari_actiu)
    elif 'tornar' in request.form:
        if es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
    personalitzades = rebre_personalitzades()
    print(personalitzades)
    return render_template('home_personalitzades_subscriure.html', personalitzades=personalitzades, usuari_actiu=usuari_actiu)





@app.route("/home/subscripcions_aventurers_personalitzades", methods=["GET", "POST"])
def home_subscripcions_aventurers_personalitzades():
    personalitzades = rebre_subscripcions_personalitzades()
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_aventurers WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        personalitzades = rebre_subscripcions_personalitzades()
        return render_template('home_subscripcions_aventurers_personalitzades.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=usuari_actiu, personalitzades=personalitzades)
    elif 'tornar' in request.form:
        if es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)
    personalitzades = rebre_subscripcions_personalitzades()
    return render_template('home_subscripcions_aventurers_personalitzades.html', personalitzades=personalitzades, usuari_actiu=usuari_actiu)

###############################
# Creació llista personalitzada
###############################

llista_activa = 0

@app.route("/home/aventurer/llista/crear", methods=["GET", "POST"])
def home_aventurer_llista_crear():
    if request.method == 'POST':
        if 'enviat' in request.form:
            titol = request.form['titol']
            nom_poblacio = request.form['nom_poblacio']
            conn = get_db_connection()
            cur = conn.cursor()
            insert_query = "INSERT INTO projecte.llistes (titol) VALUES (%s) RETURNING codi_llista;"
            cur.execute(insert_query, (titol))
            codi_llista = cur.fetchone()[0]
            conn.commit()
            insert_query = "INSERT INTO projecte.personalitzades (codi_llista, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, usuari_actiu))
            conn.commit()
            insert_query = "INSERT INTO projecte.continguts (codi_llista, nom_poblacio) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, nom_poblacio))
            conn.commit()
            cur.close()
            conn.close()
            llista_activa = codi_llista
            return redirect("http://127.0.0.1:5000/home/aventurer/llista/modificar")
        elif 'tornar' in request.form:
            if es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=usuari_actiu)             
    return render_template('home_aventurer_llista_crear.html', usuari_actiu=usuari_actiu)
