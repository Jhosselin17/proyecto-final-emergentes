from flask import render_template

def login():
    return render_template('usuarios/login.html')


def registrar():
    return render_template('usuarios/registrar.html')

