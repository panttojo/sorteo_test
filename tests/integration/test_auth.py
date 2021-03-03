# Standard Library
import json

# Third Party Stuff
import pytest
from django.urls import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_user_registration(client):
    url = reverse("auth-register")
    credentials = {
        "email": "test@test.com",
        "password": "localhost",
        "first_name": "S",
        "last_name": "K",
    }
    response = client.json.post(url, json.dumps(credentials))
    assert response.status_code == 201
    expected_keys = ["id", "email", "first_name", "last_name", "auth_token"]
    assert set(expected_keys).issubset(response.data.keys())

    assert response.data["email"] == "test@test.com"
    assert response.data["first_name"] == "S"
    assert response.data["last_name"] == "K"


def test_user_registration_with_long_first_and_last_name(client):
    url = reverse("auth-register")
    credentials = {
        "email": "test@test.com",
        "password": "localhost",
        "first_name": "S" * 121,
        "last_name": "K" * 121,
    }
    response = client.json.post(url, json.dumps(credentials))
    assert response.status_code == 400
    assert response.data["errors"][0]["field"] == "first_name"
    assert (
        response.data["errors"][0]["message"]
        == "Ensure this field has no more than 120 characters."
    )
    assert response.data["errors"][1]["field"] == "last_name"
    assert (
        response.data["errors"][1]["message"]
        == "Ensure this field has no more than 120 characters."
    )


def test_validate_password_during_registration(client):
    url = reverse("auth-register")
    credentials = {
        "email": "test@test.com",
        "password": "123456789",
        "first_name": "S",
        "last_name": "K",
    }
    response = client.json.post(url, json.dumps(credentials))
    assert response.status_code == 400
    assert response.data["errors"][0]["field"] == "password"
    assert response.data["errors"][0]["message"] == "This password is too common."


def test_user_login(client):
    url = reverse("auth-login")
    u = f.create_user(email="test@example.com", password="test")

    credentials = {"email": u.email, "password": "test"}
    response = client.json.post(url, json.dumps(credentials))
    assert response.status_code == 200
    expected_keys = ["id", "email", "first_name", "last_name", "auth_token"]
    assert set(expected_keys).issubset(response.data.keys())


def test_user_password_change(client):
    url = reverse("auth-password-change")
    current_password = "password1"
    new_password = "paSswOrd2.#$"
    user = f.create_user(email="test@example.com", password=current_password)
    change_password_payload = {
        "current_password": current_password,
        "new_password": new_password,
    }

    client.login(user=user)
    response = client.json.post(url, json.dumps(change_password_payload))
    assert response.status_code == 204
    client.logout()

    url = reverse("auth-login")
    credentials = {"email": user.email, "password": new_password}
    response = client.json.post(url, json.dumps(credentials))
    assert response.status_code == 200
    expected_keys = ["id", "email", "first_name", "last_name", "auth_token"]
    assert set(expected_keys).issubset(response.data.keys())

    user.refresh_from_db()
    assert user.check_password(new_password)
