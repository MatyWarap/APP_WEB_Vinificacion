import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.storage import Storage
from models.grape_variety import GrapeVariety
from models.container import Container  # Suponiendo que tienes un modelo 'Container'

storages = Blueprint('storages', __name__, url_prefix='/storages')

@storages.route('/')
def get_storages():
    storages_list = Storage.query.all()
    return render_template('storages/storages.html', storages=storages_list)

@storages.route('/new', methods=['POST'])
def add_storage():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista

    id_container = request.form['id_container']
    container = Container.query.get_or_404(id_container)  # Validar que el contenedor exista

    start_date = request.form['start_date']
    end_date = request.form['end_date']
    quantity = request.form['quantity']
    location = request.form['location']

    new_storage = Storage(
        id_variety=id_variety,
        id_container=id_container,
        start_date=start_date,
        end_date=end_date,
        quantity=quantity,
        location=location
    )

    db.session.add(new_storage)
    db.session.commit()

    flash('Storage added successfully', 'success')
    return redirect(url_for('storages.get_storages'))

@storages.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_storage(id):
    storage = Storage.query.get_or_404(id)

    if request.method == 'POST':
        storage.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(storage.id_variety)

        storage.id_container = request.form['id_container']
        container = Container.query.get_or_404(storage.id_container)

        storage.start_date = request.form['start_date']
        storage.end_date = request.form['end_date']
        storage.quantity = request.form['quantity']
        storage.location = request.form['location']

        db.session.commit()
        flash('Storage updated successfully', 'success')
        return redirect(url_for('storages.get_storages'))

    return render_template('storages/edit_storage.html', storage=storage)

@storages.route('/delete/<string:id>', methods=['POST'])
def delete_storage(id):
    storage = Storage.query.get_or_404(id)
    db.session.delete(storage)
    db.session.commit()
    flash('Storage deleted successfully', 'success')
    return redirect(url_for('storages.get_storages'))