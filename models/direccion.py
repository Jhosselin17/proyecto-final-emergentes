# models/direccion.py

from database import db

class Direccion(db.Model):
    __tablename__ = 'direcciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    referencia = db.Column(db.String(100))

    def __init__(self, usuario_id, direccion, referencia=None):
        self.usuario_id = usuario_id
        self.direccion = direccion
        self.referencia = referencia

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
