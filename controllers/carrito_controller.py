from flask import Blueprint, request, redirect, url_for, session, flash
from models.carrito import Carrito
from models.producto import Producto
import views.carrito_view as carrito_view
from database import db
from models.pedido import Pedido
from models.detalle_pedido import DetallePedido
from models.direccion import Direccion
from utils.generador_pdf import generar_y_guardar_factura
from database import db
from datetime import datetime


carrito_bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@carrito_bp.route('/')
def index():
    if session.get('rol') != 'cliente':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario_id = session.get('id')
    items = Carrito.query.filter_by(usuario_id=usuario_id).all()
    total = sum(item.producto.precio * item.cantidad for item in items)
    return carrito_view.index(items, total)

@carrito_bp.route('/agregar', methods=['POST'], endpoint='carrito_agregar')
def agregar():
    usuario_id = session.get('id')
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad', 1))

    if not producto_id:
        flash('Producto inválido.', 'danger')
        return redirect(url_for('cliente.inicio'))

    producto = Producto.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('cliente.inicio'))

    if cantidad > producto.stock:
        flash(f'Solo hay {producto.stock} unidades disponibles.', 'warning')
        return redirect(url_for('cliente.inicio'))

    existente = Carrito.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
    if existente:
        existente.cantidad += cantidad
    else:
        nuevo = Carrito(usuario_id, producto_id, cantidad=cantidad)
        db.session.add(nuevo)

    producto.stock -= cantidad
    db.session.add(producto)
    db.session.commit()

    flash(f'Se añadieron {cantidad} unidades de "{producto.nombre}" al carrito.', 'success')
    return redirect(url_for('cliente.inicio'))

@carrito_bp.route('/eliminar/<int:id>')
def eliminar(id):
    item = Carrito.query.get(id)
    if item and item.usuario_id == session.get('id'):
        db.session.delete(item)
        db.session.commit()
        flash('Producto eliminado del carrito.', 'success')
    else:
        flash('Acción no permitida.', 'danger')
    return redirect(url_for('carrito.index'))

@carrito_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    item = Carrito.query.get(id)
    cantidad = int(request.form.get('cantidad', 1))

    if item and item.usuario_id == session.get('id'):
        item.cantidad = cantidad
        db.session.commit()
        flash('Cantidad actualizada.', 'info')
    else:
        flash('No autorizado.', 'danger')

    return redirect(url_for('carrito.index'))

@carrito_bp.route('/confirmar', methods=['POST'])
def confirmar():
    if session.get('rol') != 'cliente':
        flash('Iniciá sesión como cliente para confirmar el pedido.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario_id = session.get('id')
    carrito = Carrito.query.filter_by(usuario_id=usuario_id).all()

    if not carrito:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('carrito.index'))

    direccion_id = request.form.get('direccion_id')
    direccion = Direccion.query.filter_by(id=direccion_id, usuario_id=usuario_id).first()
    if not direccion:
        flash('Dirección de entrega inválida.', 'danger')
        return redirect(url_for('carrito.index'))

    total = sum(item.producto.precio * item.cantidad for item in carrito)

    pedido = Pedido(
        usuario_id=usuario_id,
        direccion_id=direccion.id,
        fecha=datetime.utcnow(),
        estado='pendiente',
        metodo_pago='efectivo',
        total=total
    )
    db.session.add(pedido)
    db.session.commit()  # Commit para obtener ID del pedido

    for item in carrito:
        detalle = DetallePedido(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unit=item.producto.precio
        )
        db.session.add(detalle)
        db.session.delete(item)  # Vacía el carrito

    db.session.commit()

    # 🔹 Generar automáticamente la factura en PDF al confirmar
    generar_y_guardar_factura(pedido)

    flash('🎉 Pedido confirmado con éxito. Tu factura fue generada automáticamente.', 'success')
    return redirect(url_for('detalle_pedido.historial_cliente'))
