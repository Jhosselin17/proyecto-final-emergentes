from flask import Blueprint, redirect, url_for, flash, session, request,current_app
from models.pedido import Pedido
from models.detalle_pedido import DetallePedido
from models.producto import Producto
from models.carrito import Carrito
from flask import make_response, render_template
from xhtml2pdf import pisa
import io
import os
from models.factura import Factura 
from utils.generador_pdf import generar_y_guardar_factura

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedido_bp.route('/confirmar', methods=['POST'])
def confirmar():

    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Debes iniciar sesión como cliente para confirmar un pedido.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario_id = session['id']
    direccion_id = request.form.get('direccion_id')
    metodo_pago = request.form.get('metodo_pago', 'efectivo')

    if not direccion_id:
        flash('Debes seleccionar una dirección.', 'warning')
        return redirect(url_for('carrito.index'))

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
        })

    pedido = Pedido(
        usuario_id=usuario_id,
        total=total,
        estado='pendiente',
        metodo_pago=metodo_pago,
        direccion_id=direccion_id
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

    for item in carrito_items:
        item.delete()
    
    generar_y_guardar_factura(pedido)


    flash('¡Tu pedido fue registrado con éxito!', 'success')
    return redirect(url_for('detalle_pedido.detalle_cliente', pedido_id=pedido.id))


@pedido_bp.route('/repetir/<int:pedido_id>')
def repetir(pedido_id):
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Debes iniciar sesión como cliente para repetir un pedido.', 'warning')
        return redirect(url_for('usuario.login'))

    pedido = Pedido.query.get_or_404(pedido_id)

    if pedido.usuario_id != session['id']:
        flash('No tenés permiso para repetir este pedido.', 'danger')
        return redirect(url_for('detalle_pedido.historial_cliente'))

    detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()

    for detalle in detalles:
        existente = Carrito.query.filter_by(usuario_id=session['id'], producto_id=detalle.producto_id).first()

        if existente:
            existente.cantidad += detalle.cantidad
            existente.save()
        else:
            nuevo = Carrito(usuario_id=session['id'], producto_id=detalle.producto_id, cantidad=detalle.cantidad)
            nuevo.save()

    flash('Los productos del pedido fueron añadidos nuevamente al carrito.', 'success')
    return redirect(url_for('carrito.index'))


@pedido_bp.route('/descargar/<int:pedido_id>')
def descargar_pdf(pedido_id):
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Iniciá sesión para descargar el comprobante.', 'warning')
        return redirect(url_for('usuario.login'))

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != session['id']:
        flash('No tenés permiso para ver este pedido.', 'danger')
        return redirect(url_for('detalle_pedido.historial_cliente'))

    detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()
    html = render_template('pdf/pedido_comprobante.html', pedido=pedido, detalles=detalles)

    # Ruta del PDF
    nombre_archivo = f'pedido_{pedido.id}.pdf'
    ruta_relativa = os.path.join('facturas', nombre_archivo)
    ruta_absoluta = os.path.join(current_app.static_folder, 'facturas', nombre_archivo)

    # Asegurar carpeta
    os.makedirs(os.path.dirname(ruta_absoluta), exist_ok=True)

    # Guardar PDF físico
    with open(ruta_absoluta, 'wb') as f:
        pisa.CreatePDF(io.StringIO(html), dest=f)

    # Registrar factura si no existe
    factura = Factura.query.filter_by(pedido_id=pedido.id).first()
    if not factura:
        factura = Factura(pedido_id=pedido.id, archivo_pdf=ruta_relativa)
        factura.save()

    # Enviar PDF al navegador
    with open(ruta_absoluta, 'rb') as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={nombre_archivo}'
        return response

@pedido_bp.route('/descargar_ticket/<int:pedido_id>')
def descargar_ticket(pedido_id):
    if session.get('rol') != 'cliente' or 'id' not in session:
        flash('Iniciá sesión para descargar el ticket.', 'warning')
        return redirect(url_for('usuario.login'))

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != session['id']:
        flash('No tenés permiso para este ticket.', 'danger')
        return redirect(url_for('detalle_pedido.historial_cliente'))

    detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()
    html = render_template('pdf/pedido_ticket.html', pedido=pedido, detalles=detalles)

    result = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=result)

    response = make_response(result.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=ticket_{pedido.id}.pdf"
    return response
