from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

def admin_subscripcions_ocasionals_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.subscripcions_ocasionals ORDER BY nom_usuari;')
    continguts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_subscripcions_ocasionals_llista.html', continguts=continguts)

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

def admin_subscripcions_ocasionals_modificar():
    return render_template('admin_subscripcions_ocasionals_modificar.html')