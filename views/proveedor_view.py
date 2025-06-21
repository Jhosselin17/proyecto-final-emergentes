from flask import render_template

def index(proveedores):
    return render_template('proveedores/lista.html', proveedores=proveedores)

def nuevo():
    return render_template('proveedores/nuevo.html')

def editar(proveedor):
    return render_template('proveedores/editar.html', proveedor=proveedor)
