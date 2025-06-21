from database import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    def __init__(self, nombre, descripcion, precio, stock, imagen, categoria_id, proveedor_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre, descripcion, precio, stock, imagen, categoria_id, proveedor_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
