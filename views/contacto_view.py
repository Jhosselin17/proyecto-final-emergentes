from flask import render_template, Blueprint

contacto_view = Blueprint('contacto_view', __name__)

@contacto_view.route('/contacto')
def contacto():
    return render_template('contacto.html')
