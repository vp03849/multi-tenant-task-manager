def test_register_and_login(client):
    r = client.post("/auth/register", json={"email": "a@test.com", "password": "pw12345"})
    assert r.status_code == 201

    r = client.post("/auth/login", json={"email": "a@test.com", "password": "pw12345"})
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "a@test.com", "password": "pw12345"})
    r = client.post("/auth/login", json={"email": "a@test.com", "password": "wrong"})
    assert r.status_code == 401