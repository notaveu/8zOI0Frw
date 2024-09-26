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
    return render_template('index.html', tasks=tasks)
