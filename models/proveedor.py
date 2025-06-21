from database import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))

    productos = db.relationship('Producto', backref='proveedor', lazy=True)

    def __init__(self, nombre, contacto=None):
        self.nombre = nombre
        self.contacto = contacto

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
