import sqlite3
import json
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / "setu.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed_challenges):
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id TEXT PRIMARY KEY,
            sector TEXT NOT NULL,
            company TEXT NOT NULL,
            workflow TEXT NOT NULL,
            challenge TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS suggestions (
            id TEXT PRIMARY KEY,
            challenge_id TEXT NOT NULL,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            desc TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) AS c FROM challenges").fetchone()["c"]
    if count == 0:
        for c in seed_challenges:
            conn.execute(
                "INSERT INTO challenges (id, sector, company, workflow, challenge, tags) VALUES (?,?,?,?,?,?)",
                (c["id"], c["sector"], c["company"], c["workflow"], c["challenge"], json.dumps(c["tags"]))
            )
        conn.commit()
    conn.close()


def get_challenges():
    conn = get_db()
    rows = conn.execute("SELECT * FROM challenges").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["tags"] = json.loads(d["tags"])
        result.append(d)
    return result


def get_challenge(challenge_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM challenges WHERE id = ?", (challenge_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["tags"] = json.loads(d["tags"])
    return d


def add_challenge(company, sector, workflow, challenge, tags):
    conn = get_db()
    new_id = "c" + str(int(time.time() * 1000))
    conn.execute(
        "INSERT INTO challenges (id, sector, company, workflow, challenge, tags) VALUES (?,?,?,?,?,?)",
        (new_id, sector, company, workflow, challenge, json.dumps(tags))
    )
    conn.commit()
    conn.close()
    return new_id


def get_suggestions(challenge_id=None):
    conn = get_db()
    if challenge_id:
        rows = conn.execute(
            "SELECT * FROM suggestions WHERE challenge_id = ? ORDER BY created_at DESC", (challenge_id,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM suggestions ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_suggestion(challenge_id, name, title, desc):
    conn = get_db()
    new_id = "s" + str(int(time.time() * 1000))
    conn.execute(
        "INSERT INTO suggestions (id, challenge_id, name, title, desc, status, created_at) VALUES (?,?,?,?,?,?,?)",
        (new_id, challenge_id, name, title, desc, "pending", str(time.time()))
    )
    conn.commit()
    conn.close()
    return new_id


def mark_interested(suggestion_id):
    conn = get_db()
    conn.execute("UPDATE suggestions SET status = 'interested' WHERE id = ?", (suggestion_id,))
    conn.commit()
    conn.close()
