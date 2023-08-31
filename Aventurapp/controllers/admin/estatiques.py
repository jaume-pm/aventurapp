from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2


def admin_estatiques_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.estatiques ORDER BY codi_llista;')
    estatiques = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_estatiques_llista.html', estatiques=estatiques)


def admin_estatiques_eliminar():
    return render_template('admin_estatiques_eliminar.html')


def admin_estatiques_crear():
    return render_template('admin_estatiques_crear.html')


def admin_estatiques_modificar():
    return render_template('admin_estatiques_modificar.html')