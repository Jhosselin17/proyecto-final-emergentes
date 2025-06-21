from flask import Blueprint, request, redirect, url_for, flash
from models.categoria import Categoria
import views.categoria_view as categoria_view

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route('/')
def index():
    categorias = Categoria.query.all()
    return categoria_view.index(categorias)

@categoria_bp.route('/nuevo')
def nuevo():
    return categoria_view.nuevo()

@categoria_bp.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    if not nombre:
        flash('El nombre es obligatorio.', 'danger')
        return redirect(url_for('categoria.nuevo'))

    categoria = Categoria(nombre)
    categoria.save()
    flash('Categoría creada con éxito.', 'success')
    return redirect(url_for('categoria.index'))

@categoria_bp.route('/editar/<int:id>')
def editar(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categoria.index'))
    return categoria_view.editar(categoria)

@categoria_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categoria.index'))

    nombre = request.form['nombre']
    categoria.nombre = nombre
    categoria.save()
    flash('Categoría actualizada.', 'success')
    return redirect(url_for('categoria.index'))

@categoria_bp.route('/eliminar/<int:id>')
def eliminar(id):
    categoria = Categoria.query.get(id)
    if categoria:
        categoria.delete()
        flash('Categoría eliminada.', 'success')
    else:
        flash('Categoría no encontrada.', 'danger')
    return redirect(url_for('categoria.index'))
