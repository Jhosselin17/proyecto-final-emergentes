from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.producto import Producto 

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')



@cliente_bp.route('/inicio')
def inicio():
    if session.get('rol') != 'cliente':
        flash('Acceso denegado: solo para clientes.', 'danger')
        return redirect(url_for('usuario.login'))
    
    productos = Producto.query.all()
    return render_template('cliente/inicio.html', productos=productos)
