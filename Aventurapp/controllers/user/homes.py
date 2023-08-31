from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

# Retorna -1 si l'usuari no existeix, 0 si existeix però la contrassenya és incorrecta
# I 1 si l'usuari existeix i la contrassenya és correcte

import globals

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
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT nom_usuari FROM projecte.aventurers WHERE nom_usuari = %s"
    cur.execute(query, (nom_usuari,))
    contrassenya_user = cur.fetchone()
    cur.close()
    conn.close()
    if contrassenya_user == None:
        globals.es_aventurer = False
    else:
        globals.es_aventurer = True

def log_in():
    if request.method == 'POST':
        nom_usuari = request.form.get("nom_usuari")
        contrassenya = request.form.get("contrassenya")
        resultat = contrassenya_correcte(nom_usuari, contrassenya)
        if(resultat == 1):
            rebre_rol(nom_usuari)
            globals.usuari_actiu = nom_usuari
            if(globals.es_aventurer):
                return redirect("http://127.0.0.1:5000/home_aventurer")
            else:
                return redirect("http://127.0.0.1:5000/home_ocasional")
        elif(resultat == 0):
            return render_template('log_in.html', message="Contrassenya per a l'usuari " + nom_usuari + " incorrecta.")
        else:
            return render_template('log_in.html', message="L'usuari " + nom_usuari + " no existeix.")
    return render_template('log_in.html')


def sign_in():
    if request.method == 'POST':
        try:
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
        except psycopg2.errors.UniqueViolation:
            message = "L'usuari ja existeix. Introdueix un altre nom d'usuari."
            return render_template('sign_in.html',message=message)
    return render_template('sign_in.html')


def canviar_contrasenya():
    if request.method == 'POST':
        if 'enviat' in request.form:
            contrasenya = request.form['contrasenya']
            conn = get_db_connection()
            cur = conn.cursor()
            query = "UPDATE projecte.usuaris SET contrassenya = %s WHERE nom_usuari = %s"
            cur.execute(query, (contrasenya, globals.usuari_actiu))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('home_canviar_contrassenya.html', message = "La contrassenya s'ha actualitzat correctament.", usuari_actiu=globals.usuari_actiu)
        elif 'tornar' in request.form:
            if globals.es_aventurer:
                return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)
            else:
                return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)   
    return render_template('home_canviar_contrassenya.html')


def home_ocasional():
    return render_template('home_ocasional.html', usuari_actiu=globals.usuari_actiu)


def home_aventurer():
    return render_template('home_aventurer.html', usuari_actiu=globals.usuari_actiu)