import eventlet
eventlet.monkey_patch()  # 👈 Esto permite usar WebSocket de verdad

import os
from flask import Flask, request, render_template, session
from extensions import mail
from database import db
from models.usuario import Usuario
from models.carrito import Carrito
from flask_socketio import SocketIO

# Controladores
from controllers import usuario_controller
from controllers.admin_controller import admin_bp
from controllers.cliente_controller import cliente_bp
from controllers.producto_controller import producto_bp
from controllers.categoria_controller import categoria_bp
from controllers.proveedor_controller import proveedor_bp
from controllers.carrito_controller import carrito_bp
from controllers.pedido_controller import pedido_bp
from controllers.detalle_pedido_controller import detalle_pedido_bp
from controllers.mensaje_controller import mensaje_bp
from views.contacto_view import contacto_view
from controllers.admin_pedido_controller import admin_pedido_bp
from controllers.test_mail_controller import test_mail_bp
from controllers.dashboard_controller import dashboard_bp

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecreto"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "instance", "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de correo con Gmail SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ramosjhonatan659@gmail.com'
app.config['MAIL_PASSWORD'] = 'ledx byup nooa ffpb'
app.config['MAIL_DEFAULT_SENDER'] = 'ramosjhonatan659@gmail.com'

mail.init_app(app)
db.init_app(app)

# 🔥 Inicializar SocketIO con CORS habilitado
socketio = SocketIO(app, cors_allowed_origins="*")

# Registro de blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(detalle_pedido_bp)
app.register_blueprint(contacto_view)
app.register_blueprint(admin_pedido_bp)
app.register_blueprint(test_mail_bp)
app.register_blueprint(mensaje_bp)
app.register_blueprint(dashboard_bp)

# Activar enlaces del menú
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

# 🟢 Ejecutar con eventlet y socketio
if __name__ == "__main__":
    os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)

    with app.app_context():
        db.create_all()

        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(
                nombre='jhonatan',
                username='admin',
                password='admin',
                rol='admin'
            )
            admin.save()
            print("✔ Usuario administrador creado (usuario: admin, clave: admin123)")

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
