from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.grape_reception import GrapeReception
from models.grape_variety import GrapeVariety

receptions = Blueprint('receptions', __name__, url_prefix='/receptions')

@receptions.route('/')
def get_receptions():
    receptions_list = GrapeReception.query.all()
    return render_template('receptions/receptions.html', receptions=receptions_list)

@receptions.route('/new', methods=['POST'])
def add_reception():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista
    origin = variety.origin  # Tomar el origen de la variedad seleccionada
    quantity = request.form['quantity']
    date = request.form['date']

    new_reception = GrapeReception(
        id_variety=id_variety,
        origin=origin,
        quantity=quantity,
        date=date
    )

    db.session.add(new_reception)
    db.session.commit()

    flash('Reception added successfully', 'success')
    return redirect(url_for('receptions.get_receptions'))

@receptions.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_reception(id):
    reception = GrapeReception.query.get_or_404(id)

    if request.method == 'POST':
        reception.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(reception.id_variety)
        reception.origin = variety.origin  # Mantener el origen de la variedad
        reception.quantity = request.form['quantity']
        reception.date = request.form['date']

        db.session.commit()
        flash('Reception updated successfully', 'success')
        return redirect(url_for('receptions.get_receptions'))

    return render_template('receptions/edit_reception.html', reception=reception)

@receptions.route('/delete/<string:id>', methods=['POST'])
def delete_reception(id):
    reception = GrapeReception.query.get_or_404(id)
    db.session.delete(reception)
    db.session.commit()
    flash('Reception deleted successfully', 'success')
    return redirect(url_for('receptions.get_receptions'))