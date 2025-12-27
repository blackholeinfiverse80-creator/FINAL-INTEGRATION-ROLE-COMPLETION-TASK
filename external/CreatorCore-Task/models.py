from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Generation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    embedding = db.Column(db.JSON)  # List of floats
    score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.now())