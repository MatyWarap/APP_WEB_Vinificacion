import uuid
from models.db import db

class GrapeReception(db.Model):
    __tablename__ = 'grape_reception'
    
    id_reception = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_variety = db.Column(db.String(36), db.ForeignKey('grape_variety.id_variety'), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, id_variety, origin, quantity, date):
        self.id_variety = id_variety
        self.origin = origin
        self.quantity = quantity
        self.date = date

    def serialize(self):
        return {
            'id_reception': self.id_reception,
            'id_variety': self.id_variety,
            'origin': self.origin,
            'quantity': self.quantity,
            'date': self.date
        }