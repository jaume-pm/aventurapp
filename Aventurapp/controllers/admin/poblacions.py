from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

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

def admin_poblacions_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.poblacions ORDER BY nom_poblacio;')
    poblacions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_poblacions_llista.html', poblacions=poblacions)

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