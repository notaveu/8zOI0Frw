import pytest

import sys
sys.path.insert(0, '.')

from app import app, dao, Task

@pytest.fixture()
def client():
    with app.app_context():
        dao.delete_all()
    yield app.test_client()
    with app.app_context():
        dao.delete_all()

@pytest.fixture()
def some_tasks(client):
    print('some_tasks')
    with app.app_context():
        dao.create(Task(title='Task 1'))
        dao.create(Task(title='Task 2'))
    return client

def test_retrieve_none(client):
    response = client.get('/')
    assert b'Sem tarefas.' in response.data

def test_retrieve_some(some_tasks):
    response = some_tasks.get('/')
    assert b'Task 1' in response.data
    assert b'Task 2' in response.data

def test_create(client):
    title = 'Fugiat deserunt irure amet veniam'
    body = 'Duis eu nisi do excepteur eu'
    client.post('/create', data={
        'title': title,
        'body': body
    })
    with app.app_context():
        task = dao.get_all()[0]
    assert task.title == title
    assert task.body == body

def test_update(some_tasks):
    with app.app_context():
        tasks = dao.get_all()
    task0 = tasks[0]
    title = 'Aute Lorem magna'
    body = 'Duis velit'
    some_tasks.post('/update/' + str(tasks[1].id), data={
        'title': title,
        'body': body
    })
    with app.app_context():
        tasks = dao.get_all()
    assert tasks[0].title == task0.title
    assert tasks[0].body == task0.body
    assert tasks[1].title == title
    assert tasks[1].body == body

def test_delete(some_tasks):
    with app.app_context():
        tasks = dao.get_all()
    some_tasks.get('/delete/' + str(tasks[0].id))
    with app.app_context():
        tasks = dao.get_all()
    assert len(tasks) == 1
