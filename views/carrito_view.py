from flask import render_template
from models.direccion import Direccion
from flask import session

def index(items, total):
    usuario_id = session.get('id')
    direcciones = Direccion.query.filter_by(usuario_id=usuario_id).all()
    return render_template('carrito/carrito.html', items=items, total=total, direcciones=direcciones)
