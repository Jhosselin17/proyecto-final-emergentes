from flask import render_template

def index(productos):
    return render_template('productos/lista.html', productos=productos)

def nuevo(categorias, proveedores):
    return render_template('productos/nuevo.html', categorias=categorias, proveedores=proveedores)

def editar(producto, categorias, proveedores):
    return render_template('productos/editar.html', producto=producto, categorias=categorias, proveedores=proveedores)
