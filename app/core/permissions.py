from app.models.workspace import WorkspaceRole

ROLE_PERMISSIONS: dict[WorkspaceRole, set[str]] = {
    WorkspaceRole.owner: {
        "workspace:delete", "workspace:update", "member:invite", "member:remove",
        "member:change_role", "project:create", "project:delete", "project:update",
        "task:create", "task:update", "task:delete", "task:assign",
    },
    WorkspaceRole.admin: {
        "member:invite", "project:create", "project:delete", "project:update",
        "task:create", "task:update", "task:delete", "task:assign",
    },
    WorkspaceRole.member: {
        "task:create", "task:update", "task:assign",
    },
}

def has_permission(role: WorkspaceRole, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())