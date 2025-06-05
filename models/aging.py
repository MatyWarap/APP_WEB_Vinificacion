import uuid
from models.db import db

class Aging(db.Model):
    __tablename__ = 'aging'
    
    id_aging = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_variety = db.Column(db.String(36), db.ForeignKey('grape_variety.id_variety'), nullable=False)
    id_container = db.Column(db.String(36), db.ForeignKey('container.id_container'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)
    duration = db.Column(db.Integer)

    def __init__(self, id_variety, id_container, start_date, end_date, temperature, duration):
        self.id_variety = id_variety
        self.id_container = id_container
        self.start_date = start_date
        self.end_date = end_date
        self.temperature = temperature
        self.duration = duration

    def serialize(self):
        return {
            'id_aging': self.id_aging,
            'id_variety': self.id_variety,
            'id_container': self.id_container,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'temperature': self.temperature,
            'duration': self.duration
        }