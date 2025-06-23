from flask import render_template

def index(
    total_usuarios,
    total_productos,
    total_pedidos,
    pedidos_hoy,
    pedidos_semana,
    mensajes_totales,
    mensajes_pendientes,
    pedidos_dias,
    pedidos_totales,
    ultimos_pedidos,
    ultimos_mensajes,
    productos_bajos
):
    return render_template(
        'admin/dashboard.html',
        total_usuarios=total_usuarios,
        total_productos=total_productos,
        total_pedidos=total_pedidos,
        pedidos_hoy=pedidos_hoy,
        pedidos_semana=pedidos_semana,
        mensajes_totales=mensajes_totales,
        mensajes_pendientes=mensajes_pendientes,
        pedidos_dias=pedidos_dias,
        pedidos_totales=pedidos_totales,
        ultimos_pedidos=ultimos_pedidos,
        ultimos_mensajes=ultimos_mensajes,
        productos_bajos=productos_bajos
    )
