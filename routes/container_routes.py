from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.container import Container

containers = Blueprint('containers', __name__, url_prefix='/containers')

@containers.route('/')
def get_containers():
    containers_list = Container.query.all()
    return render_template('containers/containers.html', containers=containers_list)

@containers.route('/new', methods=['POST'])
def add_container():
    type = request.form['type']
    capacity = request.form['capacity']
    material = request.form['material']

    new_container = Container(
        type=type,
        capacity=capacity,
        material=material
    )

    db.session.add(new_container)
    db.session.commit()

    flash('Container added successfully', 'success')
    return redirect(url_for('containers.get_containers'))

@containers.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_container(id):
    container = Container.query.get_or_404(id)

    if request.method == 'POST':
        container.type = request.form['type']
        container.capacity = request.form['capacity']
        container.material = request.form['material']

        db.session.commit()
        flash('Container updated successfully', 'success')
        return redirect(url_for('containers.get_containers'))

    return render_template('containers/edit_container.html', container=container)

@containers.route('/delete/<string:id>', methods=['POST'])
def delete_container(id):
    container = Container.query.get_or_404(id)
    db.session.delete(container)
    db.session.commit()
    flash('Container deleted successfully', 'success')
    return redirect(url_for('containers.get_containers'))