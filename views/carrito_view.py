from flask import render_template

def index(items, total):
    return render_template('carrito/carrito.html', items=items, total=total)
