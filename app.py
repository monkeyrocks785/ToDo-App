from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"
    
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        todo = Todo()
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
    todo = Todo.query.all()
    return render_template('index.html', todos = todo)

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:todo_id>', methods = ['GET', 'POST'])
def update(todo_id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.get(todo_id)
        if not todo:
            return "Todo not found", 404
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(id = todo_id).first()
    return render_template('update.html', todo = todo)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)