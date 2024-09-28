import os
from flask import Flask, redirect, render_template, request, url_for
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

@app.route('/new')
def new():
    return render_template(
        'form.html',
        fab_label='Salvar',
        form_action='/create',
        form_method='POST',
        task_body='',
        task_title='',
        title='Nova tarefa'
    )

@app.route('/create', methods=['POST'])
def create():
    if valid_task(request.form['title']):
        title = request.form['title']
        body = request.form['body'].strip() if request.form['body'].strip() else None
        dao.create(Task(title=title, body=body))
        return redirect(url_for('index'))
    else:
        return render_template(
            'form.html',
            fab_label='Salvar',
            form_action='/create',
            form_method='POST',
            task_body=request.form['body'] if len(request.form['body']) else '',
            task_title=request.form['title'] if len(request.form['title']) else '',
            title='Nova tarefa'
        )

@app.route('/delete/<task_id>')
def delete(task_id):
    dao.delete_by_id(id=task_id)
    return redirect(url_for('index'))

def valid_task(title):
    return len(title) > 0
