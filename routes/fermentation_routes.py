import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.fermentation import Fermentation
from models.grape_variety import GrapeVariety
from models.container import Container  # Suponiendo que tienes un modelo 'Container'

fermentations = Blueprint('fermentations', __name__, url_prefix='/fermentations')

@fermentations.route('/')
def get_fermentations():
    fermentations_list = Fermentation.query.all()
    return render_template('fermentations/fermentations.html', fermentations=fermentations_list)

@fermentations.route('/new', methods=['POST'])
def add_fermentation():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista

    id_container = request.form['id_container']
    container = Container.query.get_or_404(id_container)  # Validar que el contenedor exista

    start_date = request.form['start_date']
    end_date = request.form['end_date']
    temperature = request.form['temperature']
    duration = request.form['duration']

    new_fermentation = Fermentation(
        id_variety=id_variety,
        id_container=id_container,
        start_date=start_date,
        end_date=end_date,
        temperature=temperature,
        duration=duration
    )

    db.session.add(new_fermentation)
    db.session.commit()

    flash('Fermentation added successfully', 'success')
    return redirect(url_for('fermentations.get_fermentations'))

@fermentations.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_fermentation(id):
    fermentation = Fermentation.query.get_or_404(id)

    if request.method == 'POST':
        fermentation.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(fermentation.id_variety)

        fermentation.id_container = request.form['id_container']
        container = Container.query.get_or_404(fermentation.id_container)

        fermentation.start_date = request.form['start_date']
        fermentation.end_date = request.form['end_date']
        fermentation.temperature = request.form['temperature']
        fermentation.duration = request.form['duration']

        db.session.commit()
        flash('Fermentation updated successfully', 'success')
        return redirect(url_for('fermentations.get_fermentations'))

    return render_template('fermentations/edit_fermentation.html', fermentation=fermentation)

@fermentations.route('/delete/<string:id>', methods=['POST'])
def delete_fermentation(id):
    fermentation = Fermentation.query.get_or_404(id)
    db.session.delete(fermentation)
    db.session.commit()
    flash('Fermentation deleted successfully', 'success')
    return redirect(url_for('fermentations.get_fermentations'))