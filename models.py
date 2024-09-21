from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500))

    def __repr__(self):
        return f'<Image {self.filename}>'
