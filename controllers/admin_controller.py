from flask import Blueprint, render_template, session, redirect, url_for, flash,request
from models.usuario import Usuario 

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    if session.get('rol') != 'admin':
        flash('Acceso denegado: solo para administradores.', 'danger')
        return redirect(url_for('usuario.login'))
    return render_template('admin/dashboard.html')

#aqui listamos a los usuarios registrados
@admin_bp.route('/usuarios')
def lista_usuarios():
    if session.get('rol') != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('usuario.login'))

    usuarios = Usuario.query.all()
    return render_template('admin/usuarios/lista.html', usuarios=usuarios)
#aqui eliminamos a los usuarios registrados
@admin_bp.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    if session.get('rol') != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('usuario.login'))

    usuario = Usuario.query.get(id)
    if usuario:
        usuario.delete()
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('admin.lista_usuarios'))

#aqui editamos a los usuarios registrados
@admin_bp.route('/usuarios/editar/<int:id>')
def editar_usuario(id):
    if session.get('rol') != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('usuario.login'))
    
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.lista_usuarios'))

    return render_template('admin/usuarios/editar.html', usuario=usuario)

@admin_bp.route('/usuarios/actualizar/<int:id>', methods=['POST'])
def actualizar_usuario(id):
    if session.get('rol') != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('usuario.login'))
    
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.lista_usuarios'))

    nombre = request.form['nombre']
    username = request.form['username']
    password = request.form['password']
    rol = request.form['rol']

    usuario.update(nombre, username, password, rol)
    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin.lista_usuarios'))
