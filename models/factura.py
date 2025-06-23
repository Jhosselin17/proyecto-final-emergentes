from database import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False, unique=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    archivo_pdf = db.Column(db.String(200), nullable=False)

    pedido = db.relationship('Pedido', backref=db.backref('factura', uselist=False))

    def __init__(self, pedido_id, archivo_pdf, fecha=None):
        self.pedido_id = pedido_id
        self.archivo_pdf = archivo_pdf
        self.fecha = fecha or datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
