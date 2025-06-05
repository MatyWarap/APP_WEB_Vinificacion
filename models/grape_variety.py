import uuid
from models.db import db

class GrapeVariety(db.Model):
    __tablename__ = 'grape_variety'
    
    id_variety = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    def __init__(self, name, origin, image=None):
        self.name = name
        self.origin = origin
        self.image = image

    def serialize(self):
        return {
            'id_variety': self.id_variety,
            'name': self.name,
            'origin': self.origin,
            'image': self.image,
        }