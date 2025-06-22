from flask import render_template

def historial_cliente(pedidos):
    return render_template('cliente/historial_pedidos.html', pedidos=pedidos)

def listar_admin(pedidos):
    return render_template('admin/pedidos/lista.html', pedidos=pedidos)

def ver_estado(pedido):
    return render_template('admin/pedidos/estado.html', pedido=pedido)
