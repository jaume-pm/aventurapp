from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2


def admin_continguts_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.continguts ORDER BY codi_llista;')
    continguts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_continguts_llista.html', continguts=continguts)


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


def admin_continguts_modificar():
    return render_template('admin_continguts_modificar.html')


def admin_continguts_eliminar():
    if request.method == 'POST':
        nom_poblacio = request.form['nom_poblacio']
        codi_llista = request.form['codi_llista']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.contingutsWHERE nom_poblacio = %s AND codi_llista = %s;"
        cur.execute(insert_query, (nom_poblacio, codi_llista))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin_continguts_eliminar.html', message= "S'ha afegit la població " 
                           + nom_poblacio + " a la llista amb codi " + str(codi_llista))
    return render_template('admin_continguts_eliminar.html')
