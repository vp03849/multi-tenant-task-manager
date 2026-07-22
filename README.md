# Task Manager Backend

A multi-tenant task management API built with FastAPI, PostgreSQL, and SQLAlchemy. Users belong to one or more workspaces, each acting as an isolated tenant boundary — projects and tasks live inside a workspace, and access is governed by role-based permissions (owner, admin, member) rather than simple login/logout access control. The project focuses on the parts of backend engineering that are easy to get wrong in real SaaS systems: correct tenant isolation, role-scoped authorization, and reproducible infrastructure via Docker and CI.

## Architecture

### Entities

| Entity | Purpose |
|---|---|
| `User` | account and credentials |
| `Workspace` | the tenant boundary — everything below it is scoped to one workspace |
| `WorkspaceMember` | join table: user ↔ workspace, carries the user's role |
| `Project` | belongs to exactly one workspace |
| `Task` | belongs to exactly one project, optionally assigned to a user |

### Relationships

```
User ──< WorkspaceMember >── Workspace ──< Project ──< Task
                                                          │
                                              (assignee) User
```

- A `User` can belong to many `Workspace`s, through `WorkspaceMember`.
- A `Workspace` is the multi-tenancy boundary. Every query below the workspace level is filtered by `workspace_id` — this is the most common place real SaaS backends leak data across tenants, and it's the part of the system this project is built around getting right.
- A `Project` always has exactly one `workspace_id`.
- A `Task` always has exactly one `project_id`, and inherits its workspace through the project.

### Roles

| Role | Typical permissions |
|---|---|
| `owner` | everything, including deleting the workspace and changing member roles |
| `admin` | manage projects, tasks, and members; cannot delete the workspace |
| `member` | create/update/assign tasks; cannot manage members or delete projects |

## Setup

### Local (no Docker)

Requires Python 3.11 and a running PostgreSQL instance.

```bash
git clone <repo-url>
cd task-manager-backend

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# edit .env with your local Postgres credentials
```

Create the database and apply migrations:

```bash
createdb taskdb
alembic upgrade head
```

Run the app:

```bash
uvicorn app.main:app --reload
```

- Health check: `http://127.0.0.1:8000/health`
- Interactive API docs: `http://127.0.0.1:8000/docs`

### Docker

Requires Docker Desktop.

```bash
docker compose up --build -d
docker compose exec app alembic upgrade head
```

- Health check: `http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`

To stop:

```bash
docker compose down
```

## API Overview

Full interactive documentation (with request/response schemas) is available at `/docs` once the app is running. Endpoints are grouped as:

- **Auth** — register, login (JWT-based)
- **Workspaces** — create workspace, invite members, list members
- **Projects** — create and list projects within a workspace
- **Tasks** — create, list (with status filtering and pagination), and update tasks within a project

Every endpoint below the auth layer requires a valid Bearer token and enforces workspace-scoped role permissions.

## Running Tests

Tests require a separate, disposable Postgres database (never the same one used for development data, since the test suite creates and drops all tables on every test run).

```bash
createdb taskmanager_test
```

Ensure `TEST_DATABASE_URL` is set in `.env`, then:

```bash
pytest -v
```

Test coverage includes:
- Registration and login
- Permission enforcement (a `member` cannot perform `admin`/`owner`-only actions)
- Cross-workspace access is blocked (non-members get `404`, not data)
- End-to-end task creation and status updates

CI runs this same suite automatically on every push via GitHub Actions (`.github/workflows/ci.yml`), against a fresh Postgres instance, followed by a Docker image build — verifying both the application logic and the container packaging independently.

## Design Decisions

**UUIDs instead of auto-incrementing integer IDs.** Sequential IDs leak information (e.g. total user count, growth rate) and are easy to enumerate across tenants. UUIDs avoid both problems and are the standard choice for any system where multiple tenants share the same tables.

**404, not 403, for non-members.** When a user isn't a member of a workspace at all, the API returns `404 Not Found` rather than `403 Forbidden`. A `403` confirms the resource exists but access is denied — which, for a user with no relationship to that workspace, discloses more than necessary. `403` is reserved for users who *are* members but lack a specific permission, where confirming the workspace's existence is already safe.

**Role-based permissions instead of a granular permissions table.** Permissions are defined as a fixed mapping from role to a set of allowed actions (`ROLE_PERMISSIONS`), rather than a fully dynamic, database-backed permissions system. For a project of this scope, three fixed roles (owner/admin/member) cover the realistic access patterns without the added complexity of a permissions-management UI or schema. This trade-off would be revisited if the system needed custom, per-workspace roles.
