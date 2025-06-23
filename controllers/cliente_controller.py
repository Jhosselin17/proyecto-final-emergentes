from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.producto import Producto
from models.direccion import Direccion

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente_bp.route('/inicio')
def inicio():
    if session.get('rol') != 'cliente':
        flash('Acceso denegado: solo para clientes.', 'danger')
        return redirect(url_for('usuario.login'))
    
    productos = Producto.query.all()
    return render_template('cliente/inicio.html', productos=productos)

# ✅ Mostrar formulario para agregar dirección
@cliente_bp.route('/direccion/agregar')
def agregar_direccion():
    if session.get('rol') != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('usuario.login'))
    
    return render_template('cliente/agregar_direccion.html')

# ✅ Guardar nueva dirección con coordenadas
@cliente_bp.route('/direccion/guardar', methods=['POST'])
def guardar_direccion():
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Iniciá sesión como cliente.', 'danger')
        return redirect(url_for('usuario.login'))

    direccion = request.form.get('direccion')
    referencia = request.form.get('referencia')
    lat = request.form.get('latitud')
    lng = request.form.get('longitud')

    if not direccion:
        flash('La dirección es obligatoria.', 'warning')
        return redirect(url_for('cliente.agregar_direccion'))

    nueva = Direccion(
        usuario_id=session['id'],
        direccion=direccion,
        referencia=referencia,
        latitud=lat if lat else None,
        longitud=lng if lng else None
    )
    nueva.save()

    flash('Dirección guardada con éxito.', 'success')
    return redirect(url_for('carrito.index'))
