from flask_login import UserMixin
from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Modelo de Usuario
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    Email = db.Column(db.String(150), unique=True)
    Name = db.Column(db.String(150))
    Password = db.Column(db.String(256), nullable=False)
    Role = db.Column(db.String(50))

    def __repr__(self):
        return f"<User {self.Username}>"

# Modelo de Integración
class Integration(db.Model):
    __tablename__ = 'integrations'

    IntegrationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    MetaUserToken = db.Column(db.String(255))
    MetaUserID = db.Column(db.String(255))
    MetaPageID = db.Column(db.String(255))
    MetaPageName = db.Column(db.String(255))
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistants.AssistantID'))
    IsTest = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Integration {self.Type}>'

# Modelo de Asistente
class Assistant(db.Model):
    __tablename__ = 'assistants'

    AssistantID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(120), nullable=False)
    OwnerID = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    Parameter1 = db.Column(db.String(255), nullable=True)
    Parameter2 = db.Column(db.String(255), nullable=True)
    Parameter3 = db.Column(db.String(255), nullable=True)
    Prompt = db.Column(db.String(1000), nullable=True)
    IsTest = db.Column(db.Boolean, nullable=False)

    # Relación con Integraciones
    integrations = db.relationship('Integration', backref='assistant', lazy=True)

    def __repr__(self):
        return f'<Assistant {self.Name}>'