from flask import Flask, request, redirect
from flask import render_template

from get_db_connection import get_db_connection;
import psycopg2

def admin():
    classes = ["poblacions", "usuaris", "aventurers", "ocasionals", "viatges", "llistes",
               "estatiques", "personalitzades", "continguts", "subscripcions_aventurers",
               "subscripcions_ocasionals"]
    return render_template('admin.html', classes=classes)

