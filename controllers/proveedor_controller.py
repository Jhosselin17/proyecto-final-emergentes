from flask import Blueprint, request, redirect, url_for, flash
from models.proveedor import Proveedor
import views.proveedor_view as proveedor_view

proveedor_bp = Blueprint('proveedor', __name__, url_prefix='/proveedores')

@proveedor_bp.route('/')
def index():
    proveedores = Proveedor.query.all()
    return proveedor_view.index(proveedores)

@proveedor_bp.route('/nuevo')
def nuevo():
    return proveedor_view.nuevo()

@proveedor_bp.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    contacto = request.form.get('contacto')
    if not nombre:
        flash('El nombre es obligatorio.', 'danger')
        return redirect(url_for('proveedor.nuevo'))

    proveedor = Proveedor(nombre, contacto)
    proveedor.save()
    flash('Proveedor registrado.', 'success')
    return redirect(url_for('proveedor.index'))

@proveedor_bp.route('/editar/<int:id>')
def editar(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        flash('Proveedor no encontrado.', 'danger')
        return redirect(url_for('proveedor.index'))
    return proveedor_view.editar(proveedor)

@proveedor_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        flash('Proveedor no encontrado.', 'danger')
        return redirect(url_for('proveedor.index'))

    proveedor.nombre = request.form['nombre']
    proveedor.contacto = request.form.get('contacto')
    proveedor.save()
    flash('Proveedor actualizado.', 'success')
    return redirect(url_for('proveedor.index'))

@proveedor_bp.route('/eliminar/<int:id>')
def eliminar(id):
    proveedor = Proveedor.query.get(id)
    if proveedor:
        proveedor.delete()
        flash('Proveedor eliminado.', 'success')
    else:
        flash('Proveedor no encontrado.', 'danger')
    return redirect(url_for('proveedor.index'))
