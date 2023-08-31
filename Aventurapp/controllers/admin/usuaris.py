from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2


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

def admin_usuaris_eliminar():
    if request.method == 'POST':
        nom_usuari = request.form['nom_usuari']
        eliminar_usuari(nom_usuari)
        return render_template('admin_usuaris_eliminar.html', message= "L'usuari " + nom_usuari + " s'ha eliminat correctament.")
    return render_template('admin_usuaris_eliminar.html')

def admin_usuaris_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.usuaris ORDER BY nom_usuari;')
    usuaris = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_usuaris_llista.html', usuaris=usuaris)