def _setup_workspace_and_project(client, headers):
    ws = client.post("/workspaces/", json={"name": "Acme"}, headers=headers).json()
    proj = client.post(f"/workspaces/{ws['id']}/projects/", json={"name": "Launch"}, headers=headers).json()
    return ws, proj

def test_happy_path_task_flow(client):
    headers = client.post("/auth/register", json={"email": "o@test.com", "password": "pw12345"})
    headers = client.post("/auth/login", json={"email": "o@test.com", "password": "pw12345"})
    headers = {"Authorization": f"Bearer {headers.json()['access_token']}"}

    ws, proj = _setup_workspace_and_project(client, headers)

    task = client.post(f"/workspaces/{ws['id']}/projects/{proj['id']}/tasks/", json={"title": "Write docs"}, headers=headers).json()
    assert task["status"] == "todo"

    r = client.patch(f"/workspaces/{ws['id']}/projects/{proj['id']}/tasks/{task['id']}", json={"status": "in_progress"}, headers=headers)
    assert r.json()["status"] == "in_progress"