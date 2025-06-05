from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.wine import Wine
from models.grape_variety import GrapeVariety  # Suponiendo que tienes un modelo 'GrapeVariety'

wines = Blueprint('wines', __name__, url_prefix='/wines')

@wines.route('/')
def get_wines():
    wines_list = Wine.query.all()
    return render_template('wines/wines.html', wines=wines_list)

@wines.route('/new', methods=['POST'])
def add_wine():
    id_variety = request.form['id_variety']
    variety = GrapeVariety.query.get_or_404(id_variety)  # Validar que la variedad exista

    name = request.form['name']
    year = request.form['year']
    price = request.form['price']

    new_wine = Wine(
        id_variety=id_variety,
        name=name,
        year=year,
        price=price
    )

    db.session.add(new_wine)
    db.session.commit()

    flash('Wine added successfully', 'success')
    return redirect(url_for('wines.get_wines'))

@wines.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_wine(id):
    wine = Wine.query.get_or_404(id)

    if request.method == 'POST':
        wine.id_variety = request.form['id_variety']
        variety = GrapeVariety.query.get_or_404(wine.id_variety)

        wine.name = request.form['name']
        wine.year = request.form['year']
        wine.price = request.form['price']

        db.session.commit()
        flash('Wine updated successfully', 'success')
        return redirect(url_for('wines.get_wines'))

    return render_template('wines/edit_wine.html', wine=wine)

@wines.route('/delete/<string:id>', methods=['POST'])
def delete_wine(id):
    wine = Wine.query.get_or_404(id)
    db.session.delete(wine)
    db.session.commit()
    flash('Wine deleted successfully', 'success')
    return redirect(url_for('wines.get_wines'))