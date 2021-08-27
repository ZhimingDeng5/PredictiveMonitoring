from fastapi import FastAPI, Header, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from uuid import uuid4

from main_master import app

client = TestClient(app)

def test_start_with_no_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == {'tasks': []}

def test_task_not_found_error():
    taskID = str(uuid4())
    response = client.get(f"/tasks/{taskID}")
    assert response.status_code == 404

def test_dashboard_not_found_error():
    taskID = str(uuid4())
    response = client.get(f"/dashboard/{taskID}")
    assert response.status_code == 404

def test_dashboard_cancellation_not_found_error():
    taskID = str(uuid4())
    response = client.delete(f"/cancel/{taskID}")
    assert response.status_code == 404

# def test_create_dashboard():
#     response = client.post(
#         "/create-dashboard",

#     )