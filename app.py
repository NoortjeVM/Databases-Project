from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL connection: adjust user, password, and db name as needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pizza_ordering'

db = SQLAlchemy(app)

# Example table (add more in models.py later if you split)
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Optional route to confirm app runs
@app.route('/')
def home():
    return 'Pizza app is running!'

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)


#to create and activate a vertual environment: 
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

