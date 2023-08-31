from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

import globals

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
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if globals.es_aventurer:
                insert_query = "INSERT INTO projecte.subscripcions_aventurers (codi_llista, nom_usuari) VALUES (%s, %s);"
            else:
                insert_query = "INSERT INTO projecte.subscripcions_ocasionals (codi_llista, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_estatiques_subscriure.html', message="T'has subscrit a la llista " + titol,
                                   usuari_actiu=globals.usuari_actiu, estatiques=estatiques)
        except psycopg2.errors.UniqueViolation:
            message = "Ja estas subscrit a aquesta llista, només et pots subscriure una vegada a cada llista."
            return render_template('home_estatiques_subscriure.html', message=message,
                                   estatiques=estatiques, usuari_actiu=globals.usuari_actiu)
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    return render_template('home_estatiques_subscriure.html', estatiques=estatiques, usuari_actiu=globals.usuari_actiu)

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
        "   FROM projecte.subscripcions_ocasionals "
        "   WHERE nom_usuari = %s"
        ") "
        "GROUP BY l.titol, l.codi_llista"
    )
    cur.execute(insert_query, (globals.usuari_actiu,))
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
    cur.execute(insert_query, (globals.usuari_actiu,))
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    return estatiques


def home_subscripcions_estatiques():
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_ocasionals WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        estatiques = rebre_subscripcions_ocasionals()
        return render_template('home_subscripcions_estatiques.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=globals.usuari_actiu, estatiques=estatiques)
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    estatiques = rebre_subscripcions_ocasionals()
    return render_template('home_subscripcions_estatiques.html', estatiques=estatiques, usuari_actiu=globals.usuari_actiu)


def home_subscripcions_aventurers_estatiques():
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_aventurers WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        estatiques = rebre_subscripcions_aventurers_estatiques()
        return render_template('home_subscripcions_aventurers_estatiques.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=globals.usuari_actiu, estatiques=estatiques)
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    estatiques = rebre_subscripcions_aventurers_estatiques()
    return render_template('home_subscripcions_aventurers_estatiques.html', estatiques=estatiques, usuari_actiu=globals.usuari_actiu)


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
    cur.execute(insert_query, (globals.usuari_actiu,))
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

def home_personalitzades_subscriure():
    if 'codi_llista' in request.form:
        personalitzades = rebre_personalitzades()
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if globals.es_aventurer:
                insert_query = "INSERT INTO projecte.subscripcions_aventurers (codi_llista, nom_usuari) VALUES (%s, %s);"
            else:
                insert_query = "INSERT INTO projecte.subscripcions_ocasionals (codi_llista, nom_usuari) VALUES (%s, %s);"
            cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_personalitzades_subscriure.html', message="T'has subscrit a la llista " + titol,
                                   usuari_actiu=globals.usuari_actiu, personalitzades=personalitzades)
        except psycopg2.errors.UniqueViolation:
            message = "Ja estas subscrit a aquesta llista, només et pots subscriure una vegada a cada llista."
            return render_template('home_personalitzades_subscriure.html', message=message,
                                   personalitzades=personalitzades, usuari_actiu=globals.usuari_actiu)
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    personalitzades = rebre_personalitzades()
    return render_template('home_personalitzades_subscriure.html', personalitzades=personalitzades, usuari_actiu=globals.usuari_actiu)



def home_subscripcions_aventurers_personalitzades():
    personalitzades = rebre_subscripcions_personalitzades()
    if 'codi_llista' in request.form:
        info = request.form['codi_llista']
        codi_llista, titol = info.split('|')
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = "DELETE FROM projecte.subscripcions_aventurers WHERE codi_llista = %s AND nom_usuari = %s;"
        cur.execute(insert_query, (codi_llista, globals.usuari_actiu,))
        conn.commit()
        cur.close()
        conn.close()
        personalitzades = rebre_subscripcions_personalitzades()
        return render_template('home_subscripcions_aventurers_personalitzades.html', message="T'has desubscrit de la llista " + titol,
                            usuari_actiu=globals.usuari_actiu, personalitzades=personalitzades)
    elif 'tornar' in request.form:
        if globals.es_aventurer:
            return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
        else:
            return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)
    personalitzades = rebre_subscripcions_personalitzades()
    return render_template('home_subscripcions_aventurers_personalitzades.html', personalitzades=personalitzades, usuari_actiu=globals.usuari_actiu)
