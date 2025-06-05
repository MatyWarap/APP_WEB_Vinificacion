import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.bottling import Bottling
from models.grape_variety import GrapeVariety
from models.wine import Wine  # Suponiendo que tienes un modelo 'Wine'
from models.container import Container  # Suponiendo que tienes un modelo 'Container'

bottlings = Blueprint('bottlings', __name__, url_prefix='/bottlings')

@bottlings.route('/')
def get_bottlings():
    bottlings_list = Bottling.query.all()
    return render_template('bottlings/bottlings.html', bottlings=bottlings_list)

@bottlings.route('/new', methods=['POST'])
def add_bottling():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista

    id_wine = request.form['id_wine']
    wine = Wine.query.get_or_404(id_wine)  # Validar que el vino exista

    id_container = request.form['id_container']
    container = Container.query.get_or_404(id_container)  # Validar que el contenedor exista

    quantity = request.form['quantity']
    date = request.form['date']

    new_bottling = Bottling(
        id_variety=id_variety,
        id_wine=id_wine,
        id_container=id_container,
        quantity=quantity,
        date=date
    )

    db.session.add(new_bottling)
    db.session.commit()

    flash('Bottling added successfully', 'success')
    return redirect(url_for('bottlings.get_bottlings'))

@bottlings.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_bottling(id):
    bottling = Bottling.query.get_or_404(id)

    if request.method == 'POST':
        bottling.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(bottling.id_variety)

        bottling.id_wine = request.form['id_wine']
        wine = Wine.query.get_or_404(bottling.id_wine)

        bottling.id_container = request.form['id_container']
        container = Container.query.get_or_404(bottling.id_container)

        bottling.quantity = request.form['quantity']
        bottling.date = request.form['date']

        db.session.commit()
        flash('Bottling updated successfully', 'success')
        return redirect(url_for('bottlings.get_bottlings'))

    return render_template('bottlings/edit_bottling.html', bottling=bottling)

@bottlings.route('/delete/<string:id>', methods=['POST'])
def delete_bottling(id):
    bottling = Bottling.query.get_or_404(id)
    db.session.delete(bottling)
    db.session.commit()
    flash('Bottling deleted successfully', 'success')
    return redirect(url_for('bottlings.get_bottlings'))