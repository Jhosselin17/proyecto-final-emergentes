from database import db
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Usa la tabla ya existente

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def __init__(self, nombre, username, password, rol):
        self.nombre = nombre
        self.username = username
        self.password = generate_password_hash(password)
        self.rol = rol

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre, username, password, rol):
        self.nombre = nombre
        self.username = username
        if password:
            self.password = generate_password_hash(password)
        self.rol = rol
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
