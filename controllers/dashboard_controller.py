from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.usuario import Usuario
from models.producto import Producto
from models.pedido import Pedido
from models.mensaje_contacto import MensajeContacto
from models.detalle_pedido import DetallePedido  # Asegurate de importar esta
from sqlalchemy import func
from datetime import datetime, timedelta
from views import dashboard_view
from database import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')

@dashboard_bp.route('/')
def index():
    if session.get('rol') != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('inicio'))

    hoy = datetime.utcnow().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    total_usuarios = Usuario.query.count()
    total_productos = Producto.query.count()
    total_pedidos = Pedido.query.count()
    pedidos_hoy = Pedido.query.filter(func.date(Pedido.fecha) == hoy).count()
    pedidos_semana = Pedido.query.filter(Pedido.fecha >= inicio_semana).count()
    mensajes_totales = MensajeContacto.query.count()
    mensajes_pendientes = MensajeContacto.query.filter_by(respondido=False).count()

    # Últimos 5 pedidos con nombre del cliente
    ultimos_pedidos = db.session.query(
        Pedido.id,
        Pedido.fecha,
        Pedido.total,
        Producto.nombre.label('producto_nombre')
    )    .join(DetallePedido, DetallePedido.pedido_id == Pedido.id)\
    .join(Producto, DetallePedido.producto_id == Producto.id)\
    .order_by(Pedido.fecha.desc())\
    .limit(5)\
    .all()

    # Últimos 5 mensajes
    ultimos_mensajes = MensajeContacto.query.order_by(MensajeContacto.fecha.desc()).limit(5).all()

    # Productos con stock bajo
    productos_bajos = Producto.query.filter(Producto.stock <= 5).order_by(Producto.stock.asc()).limit(5).all()

    return dashboard_view.index(
        total_usuarios=total_usuarios,
        total_productos=total_productos,
        total_pedidos=total_pedidos,
        pedidos_hoy=pedidos_hoy,
        pedidos_semana=pedidos_semana,
        mensajes_totales=mensajes_totales,
        mensajes_pendientes=mensajes_pendientes,
        pedidos_dias=[],            # Gráfico deshabilitado
        pedidos_totales=[],         # Gráfico deshabilitado
        ultimos_pedidos=ultimos_pedidos,
        ultimos_mensajes=ultimos_mensajes,
        productos_bajos=productos_bajos
    )
