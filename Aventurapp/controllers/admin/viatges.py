from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

import globals

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


def admin_viatges_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = 'SELECT * FROM projecte.viatges ORDER BY nom_poblacio;'
    cur.execute(insert_query,)
    viatges = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_viatges_llista.html', viatges=viatges, usuari_actiu= globals.usuari_actiu)


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


def admin_viatges_modificar():
    return render_template('admin_viatges_modificar.html')