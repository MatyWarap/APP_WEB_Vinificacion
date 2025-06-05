import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.aging import Aging
from models.grape_variety import GrapeVariety
from models.container import Container  # Suponiendo que tienes un modelo 'Container'

agings = Blueprint('agings', __name__, url_prefix='/agings')

@agings.route('/')
def get_agings():
    agings_list = Aging.query.all()
    return render_template('agings/agings.html', agings=agings_list)

@agings.route('/new', methods=['POST'])
def add_aging():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista

    id_container = request.form['id_container']
    container = Container.query.get_or_404(id_container)  # Validar que el contenedor exista

    start_date = request.form['start_date']
    end_date = request.form['end_date']
    temperature = request.form['temperature']
    duration = request.form['duration']

    new_aging = Aging(
        id_variety=id_variety,
        id_container=id_container,
        start_date=start_date,
        end_date=end_date,
        temperature=temperature,
        duration=duration
    )

    db.session.add(new_aging)
    db.session.commit()

    flash('Aging added successfully', 'success')
    return redirect(url_for('agings.get_agings'))

@agings.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_aging(id):
    aging = Aging.query.get_or_404(id)

    if request.method == 'POST':
        aging.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(aging.id_variety)

        aging.id_container = request.form['id_container']
        container = Container.query.get_or_404(aging.id_container)

        aging.start_date = request.form['start_date']
        aging.end_date = request.form['end_date']
        aging.temperature = request.form['temperature']
        aging.duration = request.form['duration']

        db.session.commit()
        flash('Aging updated successfully', 'success')
        return redirect(url_for('agings.get_agings'))

    return render_template('agings/edit_aging.html', aging=aging)

@agings.route('/delete/<string:id>', methods=['POST'])
def delete_aging(id):
    aging = Aging.query.get_or_404(id)
    db.session.delete(aging)
    db.session.commit()
    flash('Aging deleted successfully', 'success')
    return redirect(url_for('agings.get_agings'))