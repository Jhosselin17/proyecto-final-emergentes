from models.mensaje_contacto import MensajeContacto
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.mensaje_contacto import MensajeContacto
from flask_mail import Message
from extensions import mail
from flask import current_app


mensaje_bp = Blueprint('mensaje', __name__)

@mensaje_bp.route('/enviar_mensaje', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    mensaje = request.form.get('mensaje')

    if not nombre or not email or not mensaje:
        flash('Todos los campos obligatorios deben estar completos.', 'danger')
        return redirect(url_for('contacto_view.contacto'))

    nuevo_mensaje = MensajeContacto(nombre=nombre, email=email, telefono=telefono, mensaje=mensaje)
    nuevo_mensaje.save()

    flash('Tu mensaje fue enviado correctamente. ¡Gracias!', 'success')
    return redirect(url_for('contacto_view.contacto'))

@mensaje_bp.route('/admin')
def admin_lista():
    if session.get('rol') != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('inicio'))

    mensajes = MensajeContacto.query.order_by(MensajeContacto.respondido.asc(), MensajeContacto.fecha.desc()).all()
    return render_template('admin/mensajes/lista.html', mensajes=mensajes)

@mensaje_bp.route('/admin/ver/<int:id>')
def admin_ver(id):
    if session.get('rol') != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('inicio'))

    mensaje = MensajeContacto.query.get_or_404(id)
    return render_template('admin/mensajes/ver.html', mensaje=mensaje)

@mensaje_bp.route('/admin/responder/<int:id>', methods=['POST'])
def admin_responder(id):
    if session.get('rol') != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('inicio'))

    mensaje = MensajeContacto.query.get_or_404(id)
    respuesta = request.form.get('respuesta')

    if not respuesta:
        flash('La respuesta no puede estar vacía.', 'warning')
        return redirect(url_for('mensaje.admin_ver', id=id))

    try:
        msg = Message(
            subject="📬 Respuesta a tu mensaje de contacto",
            recipients=[mensaje.email],
            body=(
                f"Hola {mensaje.nombre},\n\n"
                f"Gracias por contactarte con nosotros. Valoramos que hayas tomado el tiempo de escribirnos.\n\n"
                f"A continuación, te compartimos nuestra respuesta:\n"
                f"{'_' * 40}\n"
                f"{respuesta}\n"
                f"{'_' * 40}\n\n"
                f"🙌 Nos alegra poder ayudarte. Si tenés más consultas, no dudes en escribirnos nuevamente.\n\n"
                f"Saludos cordiales,\n"
            )
        )
        mail.send(msg)
        mensaje.respondido = True
        mensaje.save()
        flash('✉️ Respuesta enviada correctamente.', 'success')
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        flash('Hubo un error al enviar la respuesta.', 'danger')

    return redirect(url_for('mensaje.admin_ver', id=id))



