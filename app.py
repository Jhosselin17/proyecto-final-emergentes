import os
from flask import Flask, request, render_template
from controllers import usuario_controller
from database import db
from flask import session
from models.carrito import Carrito

from controllers.admin_controller import admin_bp
from controllers.cliente_controller import cliente_bp
from controllers.producto_controller import producto_bp
from controllers.categoria_controller import categoria_bp
from controllers.proveedor_controller import proveedor_bp
from controllers.carrito_controller import carrito_bp


 

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecreto"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "instance", "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registro de blueprint
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(proveedor_bp)


app.register_blueprint(carrito_bp)




# Para activar enlaces del menú
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

@app.context_processor
def cantidad_carrito():
    def contar_productos():
        if session.get('rol') == 'cliente' and session.get('id'):
            items = Carrito.query.filter_by(usuario_id=session['id']).all()
            return len(items)
        return 0
    return dict(cantidad_en_carrito=contar_productos())


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
