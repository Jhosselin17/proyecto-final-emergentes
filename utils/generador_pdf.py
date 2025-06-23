import os
import io
from flask import current_app, render_template
from xhtml2pdf import pisa
from models.factura import Factura
from models.detalle_pedido import DetallePedido

def generar_y_guardar_factura(pedido):
    detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()
    html = render_template('pdf/pedido_comprobante.html', pedido=pedido, detalles=detalles)

    nombre_archivo = f'pedido_{pedido.id}.pdf'
    ruta_relativa = os.path.join('facturas', nombre_archivo)
    ruta_absoluta = os.path.join(current_app.static_folder, 'facturas', nombre_archivo)

    os.makedirs(os.path.dirname(ruta_absoluta), exist_ok=True)

    with open(ruta_absoluta, 'wb') as f:
        pisa.CreatePDF(io.StringIO(html), dest=f)

    factura = Factura.query.filter_by(pedido_id=pedido.id).first()
    if not factura:
        factura = Factura(pedido_id=pedido.id, archivo_pdf=ruta_relativa)
        factura.save()

    return ruta_relativa  # por si querés usar la ruta después
