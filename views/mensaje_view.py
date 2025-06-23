
from flask import render_template

def lista(mensajes):
    return render_template('admin/mensajes/lista.html', mensajes=mensajes)

def ver(mensaje):
    return render_template('admin/mensajes/ver.html', mensaje=mensaje)
