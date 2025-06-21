from flask import render_template

def index(categorias):
    return render_template('categorias/lista.html', categorias=categorias)

def nuevo():
    return render_template('categorias/nuevo.html')

def editar(categoria):
    return render_template('categorias/editar.html', categoria=categoria)
