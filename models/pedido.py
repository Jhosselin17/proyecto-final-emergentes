from database import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmado, enviado, entregado, cancelado
    metodo_pago = db.Column(db.String(50))  # 'efectivo', 'tarjeta', etc.
    direccion_id = db.Column(db.Integer, db.ForeignKey('direcciones.id'))

    def __init__(self, usuario_id, total, estado='pendiente', metodo_pago=None, direccion_id=None):
        self.usuario_id = usuario_id
        self.total = total
        self.estado = estado
        self.metodo_pago = metodo_pago
        self.direccion_id = direccion_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
