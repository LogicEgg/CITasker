from app import app
from db import db
from models import Event
from datetime import datetime
from sqlalchemy import select
import pytest
from unittest.mock import MagicMock
from managedb import sample_events, kill_event

@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client

def test_add_api(client):
    response = client.post("/api/add", data={
        "event": 25,
        "deadline": "Chewsday",
        "id": "aur heck"
    })
    assert b"Bad data" in response.data
    assert response.status_code == 400

def test_edit_succ(client):
    response = client.post("/api/edit/13", data={
        "_method": "PUT",
        "id": 13,
        "event": "NEW DESCRIPTION"
    })
    assert response.status_code == 302
    assert db.session.execute(select(Event).where(Event.description == "NEW DESCRIPTION"))

def test_edit_fail(client):
    response = client.post("/api/edit/999", data={
        "id": 999,
        "event": "NEW DESCRIPTION"
    })
    assert response.status_code == 400

def test_delete_api(client):
    response = client.post("/api/delete/999")
    assert b"Failed to delete" in response.data
    assert response.status_code == 400

def test_add():
    with app.app_context():
        sample_events("SEND HELP", course=1)
        assert db.session.execute(select(Event).where(Event.description == "SEND HELP")).scalar()
        
def test_fail_add():
    with app.app_context():
        with pytest.raises(ValueError):
            sample_events(1234, course="aa")

def test_del():
    with app.app_context():
        assert kill_event("SEND HELP") == "Event killed"

def test_fail_del():
    with app.app_context():
        assert kill_event("NOT A REAL EVENT") == "Event not found"
        with pytest.raises(ValueError):
            kill_event(11)