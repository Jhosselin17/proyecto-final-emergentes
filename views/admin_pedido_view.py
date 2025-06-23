from flask import render_template

def listar_admin(pedidos):
    return render_template('admin/pedidos/lista.html', pedidos=pedidos)

def ver_estado(pedido):
    return render_template('admin/pedidos/editar.html', pedido=pedido)

def ver_detalle(pedido):
    return render_template('admin/pedidos/detalle.html', pedido=pedido)
