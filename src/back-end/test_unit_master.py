from fastapi import FastAPI, Header, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from uuid import uuid4

from main_master import app

client = TestClient(app)

# Testing the GET /tasks/{id} endpoint before any processing
# Expected: 404
def test_task_not_found_error():
    taskID = str(uuid4())
    response = client.get(f"/tasks/{taskID}")
    assert response.status_code == 404

# Testing the GET /dashboard/{id} endpoint before any processing
# Expected: 404
def test_dashboard_not_found_error():
    taskID = str(uuid4())
    response = client.get(f"/dashboard/{taskID}")
    assert response.status_code == 404

# Testing the CANCEL /task/{id} endpoint before any processing
# Expected: 404
def test_dashboard_cancellation_not_found_error():
    taskID = str(uuid4())
    response = client.delete(f"/cancel/{taskID}")
    assert response.status_code == 404

# def test_create_dashboard():
#     response = client.post(
#         "/create-dashboard",

#     )