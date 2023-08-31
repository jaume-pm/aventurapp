from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2, globals

def home_viatges_crear():
    if request.method == 'POST':
        if 'enviat' in request.form:
            try:
                nom_poblacio = request.form['nom_poblacio']
                conn = get_db_connection()
                cur = conn.cursor()
                insert_query = "INSERT INTO projecte.viatges (nom_poblacio, nom_usuari) VALUES (%s, %s);"
                cur.execute(insert_query, (nom_poblacio,globals.usuari_actiu))
                conn.commit()
                cur.close()
                conn.close()
                return render_template('home_viatges_crear.html', message = "Viatge a " + nom_poblacio + " realitzat correctament.", usuari_actiu=globals.usuari_actiu)
            except psycopg2.errors.ForeignKeyViolation:
                message = "Població no vàlida. Aquesta població no és una població de Catalunya."
                return render_template('home_viatges_crear.html', message = message, usuari_actiu=globals.usuari_actiu)
        elif 'tornar' in request.form:
            if globals.es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)             
    return render_template('home_viatges_crear.html', usuari_actiu=globals.usuari_actiu)


def home_viatges_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = 'SELECT nom_poblacio FROM projecte.viatges WHERE nom_usuari = %s ORDER BY nom_poblacio;'
    cur.execute(insert_query, (globals.usuari_actiu,))
    viatges = cur.fetchall()
    cur.close()
    conn.close()
    if request.method == 'POST':
            if globals.es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
            
    return render_template('home_viatges_llista.html', viatges=viatges, usuari_actiu=globals.usuari_actiu)
