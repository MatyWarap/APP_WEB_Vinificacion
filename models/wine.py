import uuid
from models.db import db

class Wine(db.Model):
    __tablename__ = 'wine'
    
    id_wine = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_variety = db.Column(db.String(36), db.ForeignKey('grape_variety.id_variety'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __init__(self, id_variety, name, year, price):
        self.id_variety = id_variety
        self.name = name
        self.year = year
        self.price = price

    def serialize(self):
        return {
            'id_wine': self.id_wine,
            'id_variety': self.id_variety,
            'name': self.name,
            'year': self.year,
            'price': self.price
        }