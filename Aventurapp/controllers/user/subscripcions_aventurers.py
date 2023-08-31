from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

import globals

def home_aventurer_llista_crear():
    if request.method == 'POST':
        if 'enviat' in request.form:
            try:
                titol = request.form['titol']
                nom_poblacio = request.form['nom_poblacio']
                conn = get_db_connection()
                cur = conn.cursor()
                insert_query = "INSERT INTO projecte.llistes (titol) VALUES (%s) RETURNING codi_llista;"
                cur.execute(insert_query, (titol,))
                codi_llista = cur.fetchone()[0]
                conn.commit()
                insert_query = "INSERT INTO projecte.personalitzades (codi_llista, nom_usuari) VALUES (%s, %s);"
                cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
                conn.commit()
                insert_query = "INSERT INTO projecte.continguts (codi_llista, nom_poblacio) VALUES (%s, %s);"
                cur.execute(insert_query, (codi_llista, nom_poblacio,))
                conn.commit()
                cur.close()
                conn.close()
                globals.llista_activa = codi_llista
                return redirect("http://127.0.0.1:5000/home/aventurer/llista/modificar")
            except Exception:
                message = "Població no vàlida. Aquesta població no és una població de Catalunya."
                return render_template('home_aventurer_llista_crear.html', message=message, usuari_actiu=globals.usuari_actiu)
            
        elif 'tornar' in request.form:
            if globals.es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)             
    return render_template('home_aventurer_llista_crear.html', usuari_actiu=globals.usuari_actiu)

def rebre_info_llista_modificar():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol,array_agg(c.nom_poblacio) AS poblacions "
        "FROM projecte.llistes AS l "
        "JOIN projecte.personalitzades AS p ON l.codi_llista = p.codi_llista "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "WHERE l.codi_llista = %s "
        "GROUP BY l.titol"
    )
    cur.execute(insert_query, (globals.llista_activa,))
    info_personalitzada = cur.fetchone()
    cur.close()
    conn.close()
    return info_personalitzada


def home_aventurer_llista_modificar():
    if 'nom_poblacio_eliminar' in request.form:
        nom_poblacio = request.form['nom_poblacio_eliminar']
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.continguts WHERE codi_llista = %s AND nom_poblacio = %s;"
        cur.execute(insert_query, (globals.llista_activa, nom_poblacio,))
        conn.commit()
        personalitzada = rebre_info_llista_modificar()
        # If the personalitzada list is empty, delete it
        if personalitzada is None:
            insert_query = "DELETE FROM projecte.llistes WHERE codi_llista = %s;"
            cur.execute(insert_query, (globals.llista_activa,))
            conn.commit()
            cur.close()
            conn.close()
            message = "S'ha eliminat la llista."
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu, message=message)
        cur.close()
        conn.close()
        return render_template('home_aventurer_llista_modificar.html', personalitzada=personalitzada)
    
    elif 'afegir' in request.form:
        try:
            nom_poblacio = request.form['nom_poblacio_afegir']
            conn = get_db_connection()
            cur = conn.cursor()
            insert_query = "INSERT INTO projecte.continguts (codi_llista, nom_poblacio) VALUES (%s, %s)"
            cur.execute(insert_query, (globals.llista_activa, nom_poblacio,))
            conn.commit()
            cur.close()
            conn.close()
            personalitzada = rebre_info_llista_modificar()
            return render_template('home_aventurer_llista_modificar.html', personalitzada=personalitzada)
        except psycopg2.errors.UniqueViolation:
            message = "Una mateixa població només pot apareixer una vegada en una llista."
            personalitzada = rebre_info_llista_modificar()
            return render_template('home_aventurer_llista_modificar.html', personalitzada=personalitzada, message=message)
        except psycopg2.errors.ForeignKeyViolation:
            message = "Població no vàlida. Aquesta població no és una població de Catalunya."
            personalitzada = rebre_info_llista_modificar()
            return render_template('home_aventurer_llista_modificar.html', personalitzada=personalitzada, message=message)
    
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
        
    personalitzada = rebre_info_llista_modificar()  
    return render_template('home_aventurer_llista_modificar.html', usuari_actiu=globals.usuari_actiu, personalitzada=personalitzada)



def rebre_personalitzades_usuari():
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = (
        "SELECT l.titol, l.codi_llista, array_agg(c.nom_poblacio) "
        "FROM projecte.llistes AS l "
        "JOIN projecte.continguts AS c ON l.codi_llista = c.codi_llista "
        "JOIN projecte.personalitzades AS p ON l.codi_llista = p.codi_llista "
        "WHERE p.nom_usuari = %s "
        "AND l.codi_llista NOT IN ("
        "    SELECT e.codi_llista "
        "    FROM projecte.estatiques AS e"
        ") "
        "GROUP BY l.titol, l.codi_llista"
    )
    cur.execute(insert_query, (globals.usuari_actiu,))
    personalitzades = cur.fetchall()
    cur.close()
    conn.close()
    return personalitzades


def home_aventurer_llista_seleccionar():
    personalitzades = rebre_personalitzades_usuari()
    if 'codi_llista' in request.form:
        codi_llista = request.form['codi_llista']
        globals.llista_activa = codi_llista
        return redirect("http://127.0.0.1:5000/home/aventurer/llista/modificar")
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    return render_template('home_aventurer_llista_seleccionar.html', personalitzades=personalitzades, usuari_actiu=globals.usuari_actiu)