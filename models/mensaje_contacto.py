from database import db
from datetime import datetime

class MensajeContacto(db.Model):
    __tablename__ = 'mensajes_contacto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20)) 
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    respondido = db.Column(db.Boolean, default=False)

    def __init__(self, nombre, email, mensaje, telefono=None, fecha=None):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.mensaje = mensaje
        self.fecha = fecha or datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
