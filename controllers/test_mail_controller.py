from flask import Blueprint, redirect, url_for, flash, current_app
from flask_mail import Message
from extensions import mail

test_mail_bp = Blueprint('test_mail', __name__)

@test_mail_bp.route('/test-correo')
def enviar_correo_de_prueba():
    msg = Message(subject="📎 Factura de prueba",
                  recipients=['danielacopana@gmail.com'])

    msg.body = "Hola Jhonatan,\n\nEste es un correo de prueba con un archivo adjunto desde Flask-Mail."

    try:
        with current_app.open_resource("static/facturas/pedido_4.pdf") as pdf:
            msg.attach("factura_demo.pdf", "application/pdf", pdf.read())

        mail.send(msg)
        flash("✔ Correo enviado correctamente", "success")
    except Exception as e:
        print("❌ Error al enviar correo:", e)
        flash("Error al enviar el correo de prueba.", "danger")

    return redirect(url_for('home'))
