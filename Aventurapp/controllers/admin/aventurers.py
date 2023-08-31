from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

def admin_aventurers_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.aventurers ORDER BY nom_usuari;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_aventurers_llista.html', aventurers=aventurers)

def admin_aventurers_crear():
    return render_template('admin_aventurers_crear.html')

def admin_aventurers_modificar():
    return render_template('admin_aventurers_modificar.html')

def admin_aventurers_eliminar():
    return render_template('admin_aventurers_eliminar.html')