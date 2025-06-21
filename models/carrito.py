from database import db
from models.producto import Producto  # Asegurate de importar Producto aquí

class Carrito(db.Model):
    __tablename__ = 'carrito'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.String(20), nullable=False, default='pendiente') 

    # 🔗 Relación con Producto
    producto = db.relationship('Producto', backref='carritos', lazy=True)

    def __init__(self, usuario_id, producto_id, cantidad=1):
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad = cantidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, cantidad):
        self.cantidad = cantidad
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
