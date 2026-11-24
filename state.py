"""Состояние задачи в state.json: что уже сделано. Историю диалога модели хранит sessions.db."""

import json
import os
from pathlib import Path

PATH = Path("state.json")

DEFAULT = {
    "status": "new",
    "attempts": 0,
    "decision": None,
    "selected_venue": None,
    "skill_activated": False,
    "bulletin": None,
    "checkpoint": None,
    "token_usage": {},
}


GRAPH = {
    "new": {"running"},
    "running": {"waiting_approval", "done", "failed", "needs_attention"},
    "waiting_approval": {"running"},
    "done": set(),
    "failed": set(),
    "needs_attention": set(),
}


def load() -> dict:
    """Прочитать состояние; если файла ещё нет — вернуть начальное."""
    if not PATH.exists():
        return dict(DEFAULT)
    return {**DEFAULT, **json.loads(PATH.read_text(encoding="utf-8"))}


def update(**fields) -> dict:
    """Изменить поля и записать файл целиком через временный: читатель не увидит половину файла."""
    task = load()
    new_status = fields.get("status", task["status"])
    if new_status != task["status"] and new_status not in GRAPH[task["status"]]:
        raise ValueError(f"Переход {task['status']} -> {new_status} запрещён")
    task.update(fields)
    tmp = PATH.with_name("state.json.tmp")
    tmp.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, PATH)
    return task
