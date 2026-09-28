# Auth Server (login + registration)

This is a standalone Flask auth server added to the project without modifying existing project files. It provides simple login and registration pages and stores users in a local SQLite database (`users.db`).

Run locally:

```bash
python -m pip install -r auth_server/requirements.txt
python auth_server/app.py
```

Open: http://127.0.0.1:5000/login

Notes:
- The app creates `auth_server/users.db` on first run.
- Change the secret by setting environment variable `AUTH_APP_SECRET`.
