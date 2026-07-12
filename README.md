# task-manager-backend


Relationships:
User -> WorkspaceMember -> Workspace -> Project -> Task

Redis/Memcached


Entities & relationships:
 - User
 - Workspace
 - WorskspaceMember
 - Project
 - Task

Roles:
- owner
- admin 
- member

User - Who is this person?
- Email, hashed_password, is_active, created_at

Workspace - Where does this work happen?
- Eg: A company, a team, a client account
- Name, created_by, created_at

WorkspaceMember - Who can acccess WHAT, and HOW?
- user_id, workspace_id, role (owner, admin, member), joined_at

Project - What is the scope of work inside a workspace?
- name, workspace_id, created_by

Task - What is the unit of work?
- title, description, status, project_id, assigned_user_id