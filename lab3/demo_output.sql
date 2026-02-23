BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL, email TEXT);
CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY, name TEXT NOT NULL, owner_id INTEGER NOT NULL, FOREIGN KEY(owner_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, project_id INTEGER NOT NULL, assignee_id INTEGER, completed INTEGER, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(assignee_id) REFERENCES users(id));
INSERT INTO users(id, username, email) VALUES(1, 'step_user', 'step@example.com');
INSERT INTO users(id, username, email) VALUES(2, 'delegated_user', 'deleg@example.com');
INSERT INTO projects(id, name, owner_id) VALUES(3, 'Project A [label]', 1);
INSERT INTO tasks(id, title, project_id, assignee_id, completed) VALUES(4, 'Implement feature', 3, 2, 0);
COMMIT;