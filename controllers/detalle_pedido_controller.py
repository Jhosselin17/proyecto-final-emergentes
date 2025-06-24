from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.pedido import Pedido
from models.detalle_pedido import DetallePedido
from models.usuario import Usuario

detalle_pedido_bp = Blueprint('detalle_pedido', __name__, url_prefix='/detalle-pedido')

@detalle_pedido_bp.route('/<int:pedido_id>')
def detalle_cliente(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)

    if session.get('rol') != 'cliente' or session.get('id') != pedido.usuario_id:
        flash('No tienes acceso a este pedido.', 'danger')
        return redirect(url_for('cliente.inicio'))

    detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()

    cliente = Usuario.query.get(session.get('id'))  # 🔹 Ahora sí, lo pasás

    return render_template('cliente/detalle_pedido.html', pedido=pedido, detalles=detalles, cliente=cliente)


@detalle_pedido_bp.route('/historial')
def historial_cliente():
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Debes iniciar sesión para ver tus pedidos.', 'danger')
        return redirect(url_for('usuario.login'))

    pedidos = Pedido.query.filter_by(usuario_id=session['id']).order_by(Pedido.fecha.desc()).all()
    return render_template('cliente/historial_pedidos.html', pedidos=pedidos)
