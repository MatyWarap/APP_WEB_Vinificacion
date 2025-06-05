import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models.db import db
from models.grape_variety import GrapeVariety

varieties = Blueprint('varieties', __name__, url_prefix='/varieties')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@varieties.route('/')
def get_varieties():
    varieties_list = GrapeVariety.query.all()
    return render_template('varieties/varieties.html', varieties=varieties_list)


@varieties.route('/new', methods=['POST'])
def add_variety():
    name = request.form['name']
    origin = request.form['origin']

    image_file = request.files.get('image')
    filename = None

    if image_file and image_file.filename != '':
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
        else:
            flash('Image format not allowed', 'danger')
            return redirect(request.referrer)

    new_variety = GrapeVariety(
        name=name,
        origin=origin,
        image=filename
    )

    db.session.add(new_variety)
    db.session.commit()

    flash('Variety added successfully', 'success')
    return redirect(url_for('varieties.get_varieties'))


@varieties.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_variety(id):
    variety = GrapeVariety.query.get_or_404(id)

    if request.method == 'POST':
        variety.name = request.form['name']
        variety.origin = request.form['origin']

        # Manejar imagen
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # Borrar imagen vieja
                if variety.image:
                    old_image_path = os.path.join(UPLOAD_FOLDER, variety.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                # Guardar nueva imagen
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                variety.image = filename
            else:
                flash(
                    'Image format not allowed', 'danger')
                return redirect(request.referrer)

        db.session.commit()
        flash('Variety updated successfully', 'success')
        return redirect(url_for('varieties.get_varieties'))

    return render_template('varieties/edit_varieties.html', varieties=variety)


@varieties.route('/delete/<string:id>', methods=['POST'])
def delete_variety(id):
    variety = GrapeVariety.query.get_or_404(id)

    # Borrar imagen si existe
    if variety.image:
        image_path = os.path.join(UPLOAD_FOLDER, variety.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(variety)
    db.session.commit()
    flash('Variety deleted successfully', 'success')
    return redirect(url_for('varieties.get_varieties'))