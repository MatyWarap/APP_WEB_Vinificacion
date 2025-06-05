from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.about import about
from routes.grape_variety_routes import varieties
from routes.grape_reception_routes import receptions
from routes.fermentation_routes import fermentations
from routes.aging_routes import agings
from routes.bottling_routes import bottlings
from routes.storage_routes import storages
from routes.container_routes import containers
from routes.wine_routes import wines

app = Flask(__name__)
app.secret_key = 'clave_secreta'

app.register_blueprint(about)
app.register_blueprint(varieties)
app.register_blueprint(receptions)
app.register_blueprint(fermentations)
app.register_blueprint(agings)
app.register_blueprint(bottlings)
app.register_blueprint(storages)
app.register_blueprint(containers)
app.register_blueprint(wines)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.grape_variety import GrapeVariety
    from models.grape_reception import GrapeReception
    from models.fermentation import Fermentation
    from models.aging import Aging
    from models.bottling import Bottling
    from models.storage import Storage
    from models.container import Container
    from models.wine import Wine

    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)