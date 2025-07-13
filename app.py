from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"
    
@app.route('/')
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        with app.app_context():
            todo = Todo(title = title, desc = desc)
            db.session.add(todo)
            db.session.commit()
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add():
    todo = Todo.query.all()
    print(todo)
    return "hey"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)