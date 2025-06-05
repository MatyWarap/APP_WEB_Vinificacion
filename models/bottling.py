import uuid
from models.db import db

class Bottling(db.Model):
    __tablename__ = 'bottling'
    
    id_bottling = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_variety = db.Column(db.String(36), db.ForeignKey('grape_variety.id_variety'), nullable=False)
    id_wine = db.Column(db.String(36), db.ForeignKey('wine.id_wine'), nullable=False)
    id_container = db.Column(db.String(36), db.ForeignKey('container.id_container'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)

    def __init__(self, id_variety, id_wine, id_container, quantity, date):
        self.id_variety = id_variety
        self.id_wine = id_wine
        self.id_container = id_container
        self.quantity = quantity        
        self.date = date

    def serialize(self):
        return {
            'id_bottling': self.id_bottling,
            'id_variety': self.id_variety,
            'id_wine': self.id_wine,
            'id_container': self.id_container,
            'quantity': self.quantity,
            'date': self.date
        }