"""Chat UI for the harness — a self-contained, removable feature package.

Everything the chat interface needs lives under this package: its own DDL
(migrations/chat/), its own Flask blueprint, its own templates
(harness/templates/chat/) and static assets. The dependency arrow points one
way — harness.chat imports the existing harness modules, and nothing in the
existing harness imports harness.chat.

Removing the feature is deleting this package, its templates, its static
files, and the one register_blueprint() call in harness/web.py, then running
migrations/chat/999_rollback.sql.
"""
