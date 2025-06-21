from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.producto import Producto
from models.categoria import Categoria
from models.proveedor import Proveedor
import views.producto_view as producto_view

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

@producto_bp.route('/')
def index():
    if session.get('rol') != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('usuario.login'))
    
    productos = Producto.query.all()
    return producto_view.index(productos)

@producto_bp.route('/nuevo')
def nuevo():
    categorias = Categoria.query.all()
    proveedores = Proveedor.query.all()
    return producto_view.nuevo(categorias, proveedores)

@producto_bp.route('/guardar', methods=['POST'])
def guardar():
    data = request.form
    nuevo = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=float(data['precio']),
        stock=int(data['stock']),
        imagen=data.get('imagen'),
        categoria_id=int(data['categoria_id']),
        proveedor_id=int(data['proveedor_id'])
    )
    nuevo.save()
    flash('Producto creado correctamente.', 'success')
    return redirect(url_for('producto.index'))

@producto_bp.route('/editar/<int:id>')
def editar(id):
    producto = Producto.query.get(id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('producto.index'))
    categorias = Categoria.query.all()
    proveedores = Proveedor.query.all()
    return producto_view.editar(producto, categorias, proveedores)

@producto_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    producto = Producto.query.get(id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('producto.index'))
    
    data = request.form
    producto.update(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=float(data['precio']),
        stock=int(data['stock']),
        imagen=data.get('imagen'),
        categoria_id=int(data['categoria_id']),
        proveedor_id=int(data['proveedor_id'])
    )
    flash('Producto actualizado correctamente.', 'success')
    return redirect(url_for('producto.index'))

@producto_bp.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get(id)
    if producto:
        producto.delete()
        flash('Producto eliminado correctamente.', 'success')
    else:
        flash('Producto no encontrado.', 'danger')
    return redirect(url_for('producto.index'))

@producto_bp.route('/detalle/<int:id>', endpoint='detalle_cliente')
def detalle_cliente(id):
    producto = Producto.query.get_or_404(id)
    return render_template('cliente/detalle.html', producto=producto)
