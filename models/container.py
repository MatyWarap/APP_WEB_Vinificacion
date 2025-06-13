import uuid
from models.db import db

class Container(db.Model):
    __tablename__ = 'container'
    
    id_container = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(50), nullable=False)  # Ej: barrica, tanque, botella
    capacity = db.Column(db.Float, nullable=False)
    material = db.Column(db.String(50))  # Ej: acero inoxidable, roble, plástico

    def __init__(self, type, capacity, material):
        self.type = type
        self.capacity = capacity
        self.material = material

    def serialize(self):
        return {
            'id_container': self.id_container,
            'type': self.type,
            'capacity': self.capacity,
            'material': self.material
        }