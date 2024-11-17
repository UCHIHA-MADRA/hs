from flask_sqlalchemy import SQLAlchemy

# Define the database instance here, but avoid initializing or importing it directly in the models
db = SQLAlchemy()

class User(db.Model):  # Use db here to define the model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
