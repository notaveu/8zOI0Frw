import os
from flask import Flask, render_template
from dataaccess import create_db, Task

if not os.getenv('SQLALCHEMY_DATABASE_URI'):
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
dao = create_db(app)

@app.route('/')
def index():
    tasks = list(dao.get_all())
    return render_template(
        'index.html',
        fab_href='/new',
        fab_label='Nova',
        tasks=tasks,
    )

@app.route('/delete/<task_id>')
def delete(task_id):
    dao.delete_by_id(id=task_id)
    return redirect(url_for('index'))
