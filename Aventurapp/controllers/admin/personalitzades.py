from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

def admin_personalitzades_llista():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projecte.personalitzades ORDER BY codi_llista;')
    personalitzades = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_personalitzades_llista.html', personalitzades=personalitzades)


def admin_personalitzades_eliminar():
    return render_template('admin_personalitzades_eliminar.html')


def admin_personalitzades_crear():
    return render_template('admin_personalitzades_crear.html')


def admin_personalitzades_modificar():
    return render_template('admin_personalitzades_modificar.html')