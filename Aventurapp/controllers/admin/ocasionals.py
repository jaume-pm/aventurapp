from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

def admin_ocasionals_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.ocasionals ORDER BY nom_usuari;')
    aventurers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_ocasionals_llista.html', aventurers=aventurers)

def admin_ocasionals_eliminar():
    return render_template('admin_ocasionals_eliminar.html')


def admin_ocasionals_crear():
    return render_template('admin_ocasionals_crear.html')


def admin_ocasionals_modificar():
    return render_template('admin_ocasionals_modificar.html')