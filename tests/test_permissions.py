def _register_and_login(client, email):
    client.post("/auth/register", json={"email": email, "password": "pw12345"})
    r = client.post("/auth/login", json={"email": email, "password": "pw12345"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_member_cannot_invite(client):
    owner_headers = _register_and_login(client, "owner@test.com")
    ws = client.post("/workspaces/", json={"name": "Acme"}, headers=owner_headers).json()

    _register_and_login(client, "member@test.com")  # exists as a user, not yet a member
    # owner invites them as "member" role
    client.post(f"/workspaces/{ws['id']}/members", json={"email": "member@test.com", "role": "member"}, headers=owner_headers)

    member_headers = _register_and_login(client, "member@test.com")
    r = client.post(f"/workspaces/{ws['id']}/members", json={"email": "someone@test.com", "role": "member"}, headers=member_headers)
    assert r.status_code == 403

def test_cross_workspace_access_blocked(client):
    a_headers = _register_and_login(client, "a@test.com")
    b_headers = _register_and_login(client, "b@test.com")

    ws_a = client.post("/workspaces/", json={"name": "WS-A"}, headers=a_headers).json()

    # user B, who is not a member of WS-A, tries to list its members
    r = client.get(f"/workspaces/{ws_a['id']}/members", headers=b_headers)
    assert r.status_code == 404  # not 403 — B shouldn't even learn it exists