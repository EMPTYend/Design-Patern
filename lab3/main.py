from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Callable, Iterable
import inspect, os, json

# ---------------------- Utilities ----------------------
def creation_site(offset=1) -> str:
    """Return short trace of where an object was created: filename:lineno"""
    frame = inspect.stack()[offset]
    return f"{os.path.basename(frame.filename)}:{frame.lineno}"

# ---------------------- Immutable models ----------------------
@dataclass(frozen=True)
class UserImmutable:
    id: int
    username: str
    email: Optional[str]

@dataclass(frozen=True)
class ProjectImmutable:
    id: int
    name: str
    owner_id: int

@dataclass(frozen=True)
class TaskImmutable:
    id: int
    title: str
    project_id: int
    assignee_id: Optional[int]
    completed: bool

# ---------------------- Mutable models for builder ----------------------
class BaseMutable:
    _temp_counter = 1
    def __init__(self):
        self.temp_id = BaseMutable._temp_counter
        BaseMutable._temp_counter += 1
        self.creation_site = creation_site(2)
    def collect_validation(self) -> List[str]:
        return []

class UserMutable(BaseMutable):
    def __init__(self, username: str = "", email: Optional[str] = None):
        super().__init__()
        self._username = username
        self._email = email

    @property
    def username(self): return self._username
    @username.setter
    def username(self, v: str):
        if not v or not v.strip():
            raise ValueError("username cannot be empty")
        self._username = v.strip()

    @property
    def email(self): return self._email
    @email.setter
    def email(self, v: Optional[str]):
        if v is not None and "@" not in v:
            raise ValueError("email seems invalid")
        self._email = v

    def collect_validation(self) -> List[str]:
        errs = []
        if not self._username or not self._username.strip():
            errs.append("username empty")
        if self._email is not None and "@" not in self._email:
            errs.append("email invalid")
        return [f"{self.creation_site} - User(temp_id={self.temp_id}): {e}" for e in errs]

class ProjectMutable(BaseMutable):
    def __init__(self, name: str = "", owner: Optional[UserMutable] = None):
        super().__init__()
        self._name = name
        self._owner = owner

    @property
    def name(self): return self._name
    @name.setter
    def name(self, v: str):
        if not v or not v.strip():
            raise ValueError("project name cannot be empty")
        self._name = v.strip()

    @property
    def owner(self): return self._owner
    @owner.setter
    def owner(self, v: UserMutable):
        if v is None:
            raise ValueError("project owner cannot be None")
        self._owner = v

    def collect_validation(self) -> List[str]:
        errs = []
        if not self._name or not self._name.strip():
            errs.append("name empty")
        if not self._owner:
            errs.append("owner missing")
        nested = []
        if self._owner:
            nested.extend(self._owner.collect_validation())
        return [f"{self.creation_site} - Project(temp_id={self.temp_id}): {e}" for e in errs] + nested

class TaskMutable(BaseMutable):
    def __init__(self, title: str = "", project: Optional[ProjectMutable] = None, assignee: Optional[UserMutable] = None):
        super().__init__()
        self._title = title
        self._project = project
        self._assignee = assignee
        self._completed = False

    @property
    def title(self): return self._title
    @title.setter
    def title(self, v: str):
        if not v or not v.strip():
            raise ValueError("task title cannot be empty")
        self._title = v.strip()

    @property
    def project(self): return self._project
    @project.setter
    def project(self, v: ProjectMutable):
        if v is None:
            raise ValueError("task project cannot be None")
        self._project = v

    @property
    def assignee(self): return self._assignee
    @assignee.setter
    def assignee(self, v: Optional[UserMutable]):
        self._assignee = v

    def mark_done(self):
        self._completed = True

    def collect_validation(self) -> List[str]:
        errs = []
        if not self._title or not self._title.strip():
            errs.append("title empty")
        if not self._project:
            errs.append("project missing")
        nested = []
        if self._project:
            nested.extend(self._project.collect_validation())
        if self._assignee:
            nested.extend(self._assignee.collect_validation())
        formatted = [f"{self.creation_site} - Task(temp_id={self.temp_id}): {e}" for e in errs]
        return formatted + nested

# ---------------------- Abstract builder pattern ----------------------
class AbstractBuilder:
    def __init__(self):
        self.model = None
    def build(self, final_id: int, id_map: Dict[int,int]) -> Any:
        raise NotImplementedError()

class UserBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.model = UserMutable()

    # fluent setters
    def username(self, name: str):
        self.model.username = name
        return self

    def email(self, email: str):
        self.model.email = email
        return self

    def build(self, final_id: int, id_map: Dict[int,int] = None) -> UserImmutable:
        errs = self.model.collect_validation()
        if errs:
            raise ValueError("User validation failed: " + "; ".join(errs))
        return UserImmutable(id=final_id, username=self.model.username, email=self.model.email)

class ProjectBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.model = ProjectMutable()

    def name(self, name: str):
        self.model.name = name
        return self

    def owner(self, owner: UserMutable):
        self.model.owner = owner
        return self

    def build(self, final_id: int, id_map: Dict[int,int]) -> ProjectImmutable:
        errs = self.model.collect_validation()
        if errs:
            raise ValueError("Project validation failed: " + "; ".join(errs))
        owner_id = id_map[self.model._owner.temp_id]
        return ProjectImmutable(id=final_id, name=self.model.name, owner_id=owner_id)

class TaskBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.model = TaskMutable()

    def title(self, title: str):
        self.model.title = title
        return self

    def project(self, project: ProjectMutable):
        self.model.project = project
        return self

    def assignee(self, user: Optional[UserMutable]):
        self.model.assignee = user
        return self

    def completed(self, done: bool = True):
        if done:
            self.model.mark_done()
        return self

    def build(self, final_id: int, id_map: Dict[int,int]) -> TaskImmutable:
        errs = self.model.collect_validation()
        if errs:
            raise ValueError("Task validation failed: " + "; ".join(errs))
        proj_id = id_map[self.model._project.temp_id]
        assignee_id = id_map[self.model._assignee.temp_id] if self.model._assignee else None
        return TaskImmutable(id=final_id, title=self.model._title, project_id=proj_id, assignee_id=assignee_id, completed=self.model._completed)

# ---------------------- Delegate configurator ----------------------
def delegate_configure(obj: Any, configurator: Optional[Callable[[Any], None]] = None) -> Any:
    if configurator:
        configurator(obj)
    return obj

# ---------------------- Scope pattern ----------------------
class ScopeConfigurator:
    def __init__(self, objects: Iterable[Any], applier: Callable[[Any], None]):
        self.objects = list(objects)
        self.applier = applier
    def __enter__(self):
        for o in self.objects:
            self.applier(o)
        return self.objects
    def __exit__(self, exc_type, exc, tb):
        return False

# ---------------------- Database builder: map temp_id -> final ids, produce SQL ----------------------
class DatabaseBuilder:
    def __init__(self):
        self._id_map: Dict[int,int] = {}
        self._next_id = 1
        self._sql_parts: List[str] = []

    def _alloc(self) -> int:
        v = self._next_id; self._next_id += 1; return v

    def persist(self, users: List[UserMutable], projects: List[ProjectMutable], tasks: List[TaskMutable], out_path: str = "/mnt/data/demo_output.sql") -> Tuple[bool, str]:
        # aggregate validations for all objects (don't stop at first)
        errors: List[str] = []
        for u in users:
            errors.extend(u.collect_validation())
        for p in projects:
            errors.extend(p.collect_validation())
        for t in tasks:
            errors.extend(t.collect_validation())

        if errors:
            return False, "Validation failed:\n" + "\n".join(errors)

        # allocate IDs and produce SQL INSERTs (no direct references in objects)
        users_sql: List[str] = []
        projects_sql: List[str] = []
        tasks_sql: List[str] = []

        for u in users:
            fid = self._alloc(); self._id_map[u.temp_id] = fid
            username_safe = u.username.replace("'", "''")
            if u.email:
                email_safe = u.email.replace("'", "''")
                email_val = "'" + email_safe + "'"
            else:
                email_val = "NULL"
            users_sql.append(f"INSERT INTO users(id, username, email) VALUES({fid}, '{username_safe}', {email_val});")

        for p in projects:
            fid = self._alloc(); self._id_map[p.temp_id] = fid
            name_safe = p._name.replace("'", "''")
            owner_id = self._id_map[p._owner.temp_id]
            projects_sql.append(f"INSERT INTO projects(id, name, owner_id) VALUES({fid}, '{name_safe}', {owner_id});")

        for t in tasks:
            fid = self._alloc(); self._id_map[t.temp_id] = fid
            title_safe = t._title.replace("'", "''")
            proj_id = self._id_map[t._project.temp_id]
            assignee_val = "NULL"
            if t._assignee:
                assignee_val = str(self._id_map[t._assignee.temp_id])
            completed_val = "1" if t._completed else "0"
            tasks_sql.append(f"INSERT INTO tasks(id, title, project_id, assignee_id, completed) VALUES({fid}, '{title_safe}', {proj_id}, {assignee_val}, {completed_val});")

        sql = "\n".join([
            "BEGIN TRANSACTION;",
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL, email TEXT);",
            "CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY, name TEXT NOT NULL, owner_id INTEGER NOT NULL, FOREIGN KEY(owner_id) REFERENCES users(id));",
            "CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, project_id INTEGER NOT NULL, assignee_id INTEGER, completed INTEGER, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(assignee_id) REFERENCES users(id));",
            *users_sql, *projects_sql, *tasks_sql,
            "COMMIT;"
        ])

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(sql)

        return True, f"OK: SQL written to {out_path}"

# ---------------------- Functional (immutable-only) builder example ----------------------
@dataclass(frozen=True)
class TaskImmutableBuilder:
    """Example of building a TaskImmutable in a Linq-like immutable chain."""
    title: str = ""
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    completed: bool = False

    def with_title(self, title: str) -> "TaskImmutableBuilder":
        return TaskImmutableBuilder(title=title, project_id=self.project_id, assignee_id=self.assignee_id, completed=self.completed)

    def with_project(self, project_id: int) -> "TaskImmutableBuilder":
        return TaskImmutableBuilder(title=self.title, project_id=project_id, assignee_id=self.assignee_id, completed=self.completed)

    def with_assignee(self, assignee_id: Optional[int]) -> "TaskImmutableBuilder":
        return TaskImmutableBuilder(title=self.title, project_id=self.project_id, assignee_id=assignee_id, completed=self.completed)

    def mark_done(self) -> "TaskImmutableBuilder":
        return TaskImmutableBuilder(title=self.title, project_id=self.project_id, assignee_id=self.assignee_id, completed=True)

    def build(self, final_id: int) -> TaskImmutable:
        if not self.title or not self.title.strip():
            raise ValueError("title empty for immutable task builder")
        if self.project_id is None:
            raise ValueError("project_id missing for immutable task builder")
        return TaskImmutable(id=final_id, title=self.title, project_id=self.project_id, assignee_id=self.assignee_id, completed=self.completed)

# ---------------------- Demo: main() ----------------------
def main():
    print("Demo: builders system\n")

    # One-step initialization (direct immutable creation)
    immutable_user = UserImmutable(id=1, username="one_step_user", email="one@step.example")
    print("One-step immutable user:", immutable_user)

    # Stepwise initialization using mutable + builder
    user_b = UserBuilder().username("step_user").email("step@example.com")
    user_mut = user_b.model  # mutable model
    print("Mutable user created at:", user_mut.creation_site, "temp_id=", user_mut.temp_id)

    # Another user via builder but configure via delegate
    user_b2 = UserBuilder().username("delegated_user")
    delegate_configure(user_b2.model, lambda u: setattr(u, "email", "deleg@example.com"))
    user_mut2 = user_b2.model

    # Project built stepwise
    proj_b = ProjectBuilder().name("Project A").owner(user_mut)
    proj_mut = proj_b.model

    # Task built stepwise, fluent chaining
    task_b = TaskBuilder().title("Implement feature").project(proj_mut).assignee(user_mut2).completed(False)
    task_mut = task_b.model

    print("\nObjects created (mutable):")
    print(" User1:", user_mut.temp_id, user_mut.creation_site, user_mut._username, user_mut._email)
    print(" User2:", user_mut2.temp_id, user_mut2.creation_site, user_mut2._username, user_mut2._email)
    print(" Project:", proj_mut.temp_id, proj_mut.creation_site, proj_mut._name, "owner temp_id:", proj_mut._owner.temp_id)
    print(" Task:", task_mut.temp_id, task_mut.creation_site, task_mut._title, "project temp_id:", task_mut._project.temp_id, "assignee temp_id:", task_mut._assignee.temp_id)

    # Scope pattern: apply a label to multiple projects at once
    def add_label(p: ProjectMutable):
        p.name = p.name + " [label]" if "[label]" not in p.name else p.name
    with ScopeConfigurator([proj_mut], add_label):
        pass
    print("Project after scope applied:", proj_mut._name)

    # Validation demo: create a broken user and a broken task to show aggregated errors
    bad_user = UserMutable(username="", email="bademail")  # invalid username and invalid email (missing @)
    bad_project = ProjectMutable(name="", owner=None)  # invalid
    bad_task = TaskMutable(title="", project=None)  # invalid

    # Aggregate lists
    users = [user_mut, user_mut2, bad_user]
    projects = [proj_mut, bad_project]
    tasks = [task_mut, bad_task]

    # Database persistence attempt
    db = DatabaseBuilder()
    ok, msg = db.persist(users=users, projects=projects, tasks=tasks)
    print("\nDB persist attempt (with invalid objects):", ok)
    print(msg)

    # Persist only valid subset
    db2 = DatabaseBuilder()
    valid_users = [user_mut, user_mut2]
    valid_projects = [proj_mut]
    valid_tasks = [task_mut]
    ok2, msg2 = db2.persist(
    users=valid_users,
    projects=valid_projects,
    tasks=valid_tasks,
    out_path="demo_output.sql"  # сохраняем рядом с main.py
)

    print("\nDB persist valid subset:", ok2)
    print(msg2)
    if ok2:
        print("SQL file written to /mnt/data/demo_output.sql")

    # Demonstrate immutable-only builder (functional style)
    func_builder = TaskImmutableBuilder().with_title("Immutable Task").with_project(100).with_assignee(None).mark_done()
    immutable_task = func_builder.build(final_id=500)
    print("\nImmutable-only builder result:", immutable_task)

if __name__ == "__main__":
    main()

# Run the demo when executed in this environment
main()
