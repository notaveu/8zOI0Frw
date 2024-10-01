import pytest
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, '.')

daoMock = Mock()
createdbMock = Mock(return_value=daoMock)
TaskMock = Mock()
dataaccessMock = Mock(create_db=createdbMock, Task=TaskMock)

with patch('dataaccess.create_db', createdbMock):
    with patch('dataaccess.Task', TaskMock):
        from app import app, dao

@pytest.fixture()
def client():
    daoMock.get_all.return_value = []
    TaskMock.reset_mock()
    return app.test_client()

@pytest.fixture()
def some_tasks(client):
    daoMock.get_all.return_value = [
        Mock(id=1, title='Task 1'),
        Mock(id=2, title='Task 2')
    ]
    return client

def test_retrieve_none(client):
    response = client.get('/')
    assert b'Sem tarefas.' in response.data

def test_retrieve_some(some_tasks):
    response = some_tasks.get('/')
    assert b'Task 1' in response.data
    assert b'Task 2' in response.data

def test_create(client):
    # given
    TaskMock.return_value = Mock()
    daoMock.create = Mock()
    title = 'Fugiat deserunt irure amet veniam'
    body = 'Duis eu nisi do excepteur eu'
    # when
    client.post('/create', data={
        'title': title,
        'body': body
    })
    # then
    TaskMock.assert_called_once_with(title=title, body=body, completed=False)
    daoMock.create.assert_called_once_with(TaskMock.return_value)

def test_update(some_tasks):
    # given
    TaskMock.return_value = Mock()
    daoMock.update = Mock()
    tasks = dao.get_all()
    title = 'Aute Lorem magna'
    body = 'Duis velit'
    # when
    some_tasks.post('/update/' + str(tasks[1].id), data={
        'title': title,
        'body': body,
        'completed': 'on'
    })
    # then
    TaskMock.assert_called_once_with(
        id=str(tasks[1].id),
        title=title,
        body=body,
        completed=True
    )
    daoMock.update.assert_called_once_with(TaskMock.return_value)

def test_delete(some_tasks):
    # given
    daoMock.delete_by_id = Mock()
    tasks = dao.get_all()
    # when
    some_tasks.get('/delete/' + str(tasks[0].id))
    # then
    daoMock.delete_by_id.assert_called_once_with(id=str(tasks[0].id))
