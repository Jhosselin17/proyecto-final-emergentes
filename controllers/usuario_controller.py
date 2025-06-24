from flask import Blueprint, request, redirect, url_for, flash, session
from models.usuario import Usuario
import views.usuario_view as usuario_view

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

def normalizar_celular(celular):
    if celular:
        celular = celular.strip().replace(' ', '').replace('+', '')
        if not celular.startswith('591'):
            celular = '591' + celular
    return celular

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.get_by_username(username)

        if not usuario or not usuario.verificar_password(password):
            flash('Credenciales inválidas.', 'danger')
            return redirect(url_for('usuario.login'))

        # Guardar datos en sesión
        session['id'] = usuario.id
        session['rol'] = usuario.rol
        session['nombre'] = usuario.nombre

        flash(f'Bienvenido, {usuario.nombre}', 'success')

        if usuario.rol == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('cliente.inicio'))

    return usuario_view.login()

@usuario_bp.route('/registrar')
def registrar():
    return usuario_view.registrar()

@usuario_bp.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    username = request.form['username']
    password = request.form['password']
    correo = request.form.get('correo')
    celular = normalizar_celular(request.form.get('celular'))
    rol = "cliente"

    if not nombre or not username or not password:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('usuario.registrar'))

    existente = Usuario.get_by_username(username)
    if existente:
        flash('El nombre de usuario ya existe.', 'warning')
        return redirect(url_for('usuario.registrar'))

    nuevo_usuario = Usuario(nombre, username, password, rol, correo=correo, celular=celular)
    nuevo_usuario.save()
    flash('Usuario creado correctamente.', 'success')
    return redirect(url_for('usuario.login'))

@usuario_bp.route('/editar/<int:id>')
def editar(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('usuario.login'))
    return usuario_view.edit(usuario)

@usuario_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario.nombre = request.form['nombre']
    usuario.username = request.form['username']
    usuario.rol = request.form['rol']
    usuario.correo = request.form.get('correo')
    usuario.celular = normalizar_celular(request.form.get('celular'))

    nueva_contrasena = request.form['password']
    if nueva_contrasena:
        usuario.set_password(nueva_contrasena)  # Asegúrate de tener este método en el modelo

    usuario.save()  # O db.session.commit() si lo estás manejando directamente

    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin.lista_usuarios'))  # Corrige esto si estabas redirigiendo al login por error


@usuario_bp.route('/eliminar/<int:id>')
def eliminar(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        usuario.delete()
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('usuario.login'))
