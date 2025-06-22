from flask import render_template

def detalle_cliente(pedido, detalles):
    return render_template('cliente/detalle_pedido.html', pedido=pedido, detalles=detalles)

def detalle_admin(pedido, detalles):
    return render_template('admin/pedidos/detalle.html', pedido=pedido, detalles=detalles)
