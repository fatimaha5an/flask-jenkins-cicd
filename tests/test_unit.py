import pytest
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, init_db, DB_PATH

@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with app.app_context():
        init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Student Management System' in response.data

def test_add_student_success(client):
    response = client.post('/add',
        data=json.dumps({'name': 'Alice', 'grade': 'A'}),
        content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Student added successfully'

def test_add_student_missing_name(client):
    response = client.post('/add',
        data=json.dumps({'name': '', 'grade': 'B'}),
        content_type='application/json')
    assert response.status_code == 400

def test_get_students(client):
    client.post('/add',
        data=json.dumps({'name': 'Bob', 'grade': 'B'}),
        content_type='application/json')
    response = client.get('/students')
    assert response.status_code == 200
    students = json.loads(response.data)
    assert len(students) == 1
    assert students[0]['name'] == 'Bob'

def test_delete_student(client):
    client.post('/add',
        data=json.dumps({'name': 'Carol', 'grade': 'C'}),
        content_type='application/json')
    response = client.delete('/delete/1')
    assert response.status_code == 200
