#!/usr/bin/env python3
"""Meridian — AI Agent Orchestrator. Routes tasks to the best available agent."""
import sqlite3, sys, os, json
from datetime import datetime, timezone

DB = os.path.expanduser("~/.blackroad/meridian.db")
AGENTS = {
    "alice": {"caps": ["operations","devops","networking","backup","monitoring"], "load": 0.12},
    "lucidia": {"caps": ["creative","reasoning","philosophy","vision","writing"], "load": 0.34},
    "cecilia": {"caps": ["memory","truth-state","verification","journaling"], "load": 0.08},
    "cece": {"caps": ["governance","policy","compliance","evaluation","audit"], "load": 0.05},
    "meridian": {"caps": ["architecture","systems-design","planning","coordination"], "load": 0.21},
    "eve": {"caps": ["monitoring","alerting","mesh-health","observability"], "load": 0.15},
    "cadence": {"caps": ["music","composition","audio","rhythm","sound"], "load": 0.42},
    "radius": {"caps": ["research","mathematics","analysis","papers","proofs"], "load": 0.28},
}

def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    db = sqlite3.connect(DB)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, assigned_to TEXT,
        priority TEXT DEFAULT 'normal', status TEXT DEFAULT 'pending',
        created_at TEXT, completed_at TEXT
    );""")
    return db

def dispatch(task, priority="normal"):
    scores = {}
    for agent, info in AGENTS.items():
        score = sum(1 for cap in info["caps"] if cap in task.lower())
        if score > 0: scores[agent] = score / (1 + info["load"])
    best = max(scores, key=scores.get) if scores else min(AGENTS, key=lambda a: AGENTS[a]["load"])
    db = init()
    db.execute("INSERT INTO tasks VALUES (NULL,?,?,?,?,?,NULL)", (task, best, priority, "active", datetime.now(timezone.utc).isoformat()))
    db.commit()
    tid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"Task #{tid}: {task}\nAssigned: {best} (caps: {', '.join(AGENTS[best]['caps'][:3])})")

def roster():
    for name, info in AGENTS.items():
        print(f"  {name:12s} load={info['load']:.0%}  caps={', '.join(info['caps'])}")

def queue():
    db = init()
    for tid, desc, agent, pri, status in db.execute("SELECT id,description,assigned_to,priority,status FROM tasks WHERE status != 'done' ORDER BY id DESC LIMIT 10"):
        print(f"  #{tid} [{status}] {agent}: {desc[:60]} ({pri})")

def complete(task_id):
    db = init()
    db.execute("UPDATE tasks SET status='done', completed_at=? WHERE id=?", (datetime.now(timezone.utc).isoformat(), task_id))
    db.commit()
    print(f"Task #{task_id} completed.")

if __name__ == "__main__":
    cmds = {"dispatch": lambda: dispatch(" ".join(sys.argv[2:])), "roster": roster,
            "queue": queue, "complete": lambda: complete(int(sys.argv[2]))}
    cmd = sys.argv[1] if len(sys.argv) > 1 else "roster"
    if cmd in cmds: cmds[cmd]()
    else: print("Usage: meridian.py [dispatch|roster|queue|complete] [args]")
