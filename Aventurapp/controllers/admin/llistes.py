from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2, globals

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
    cur.close()
    conn.close()
    return int(codi_llista)

def crear_estatica(codi_llista):
    conn = get_db_connection()
    cur = conn.cursor()
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


def admin_llistes_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.llistes ORDER BY codi_llista;')
    llistes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_llistes_llista.html', llistes=llistes)




def admin_llistes_modificar():
    if request.method == 'POST':
        if 'rebre_valors' in request.form:
            codi_llista_objectiu = request.form['codi_llista_objectiu']
            titol = rebre_info_llista_titol(codi_llista_objectiu)
            globals.personalitzada = es_personalitzada(codi_llista_objectiu)
            if globals.personalitzada:
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
            if globals.personalitzada:
                creador = request.form['creador']
                actualitzar_personalitzada(codi_llista_objectiu, codi_llista, titol, creador)
            else:
                actualitzar_estatica(codi_llista_objectiu, codi_llista, titol)
            return render_template('admin_llistes_modificar.html', message="Dades de la llista " + str(codi_llista) + " amb títol " + titol + " actualitzades.")
        
    return render_template('admin_llistes_modificar.html')

def admin_llistes_eliminar():
    if request.method == 'POST':
        codi_llista = request.form['codi_llista']
        eliminar_llista(codi_llista)
        return render_template('admin_llistes_eliminar.html', message= "La llista " + codi_llista + " s'ha eliminat correctament.")
    return render_template('admin_llistes_eliminar.html')
