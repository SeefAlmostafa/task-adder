from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Constant error messages
ERROR_ADD_TASK = 'There was an issue adding your task'
ERROR_DELETE_TASK = 'There was a problem deleting that task'
ERROR_UPDATE_TASK = 'There was an issue updating your task'
ERROR_EMPTY_CONTENT = 'Task content cannot be empty'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'].strip()

        if task_content:
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return ERROR_ADD_TASK
        else:
            return ERROR_EMPTY_CONTENT

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return ERROR_DELETE_TASK

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        new_content = request.form['content'].strip()

        # Check if the updated content is not empty before updating
        if new_content:
            task_to_update.content = new_content

            try:
                db.session.commit()
                return redirect('/')
            except:
                return ERROR_UPDATE_TASK
        else:
            return ERROR_EMPTY_CONTENT

    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)