from flask import Blueprint, redirect, url_for, flash, session
from models.pedido import Pedido
from models.detalle_pedido import DetallePedido
from models.producto import Producto
from models.carrito import Carrito

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedido_bp.route('/confirmar', methods=['POST'])
def confirmar():
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Debes iniciar sesión como cliente para confirmar un pedido.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario_id = session['id']
    carrito_items = Carrito.query.filter_by(usuario_id=usuario_id).all()

    if not carrito_items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('carrito.index'))

    total = 0
    detalles = []

    for item in carrito_items:
        producto = Producto.query.get(item.producto_id)

        if not producto or producto.stock < item.cantidad:
            flash(f"No hay suficiente stock para {producto.nombre}.", 'danger')
            return redirect(url_for('carrito.index'))

        subtotal = item.cantidad * producto.precio
        total += subtotal

        detalles.append({
            'producto_id': producto.id,
            'cantidad': item.cantidad,
            'precio_unit': producto.precio,
            'subtotal': subtotal
        })

    pedido = Pedido(
        usuario_id=usuario_id,
        total=total,
        estado='pendiente',
        metodo_pago='efectivo'
    )
    pedido.save()

    for d in detalles:
        detalle = DetallePedido(
            pedido_id=pedido.id,
            producto_id=d['producto_id'],
            cantidad=d['cantidad'],
            precio_unit=d['precio_unit']
        )
        detalle.save()

        producto = Producto.query.get(d['producto_id'])
        producto.stock -= d['cantidad']
        producto.save()

    # Limpiar carrito del cliente después del pedido
    for item in carrito_items:
        item.delete()

    flash('¡Tu pedido fue registrado con éxito!', 'success')
    return redirect(url_for('detalle_pedido.detalle_cliente', pedido_id=pedido.id))
