import sqlite3, time

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY,
            int_id INTEGER UNIQUE,
            text_chunk TEXT,
            created_at INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS id_map (
            int_id INTEGER PRIMARY KEY,
            msg_id TEXT UNIQUE
        )
    """)
    conn.commit()
    return conn


def next_int_id(conn):
    row = conn.execute("SELECT MAX(int_id) FROM id_map").fetchone()
    if row[0] is None:
        return 1
    return row[0] + 1


def insert_chunk(conn, msg_id, int_id, text_chunk):
    conn.execute(
        "INSERT INTO memory(id,int_id,text_chunk,created_at) VALUES (?,?,?,?)",
        (msg_id, int_id, text_chunk, int(time.time()))
    )
    conn.execute(
        "INSERT INTO id_map(int_id,msg_id) VALUES(?,?)",
        (int_id, msg_id)
    )
    conn.commit()


def fetch_chunks_by_ids(conn, ids):
    if not ids:
        return []
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"SELECT text_chunk FROM memory WHERE int_id IN ({placeholders})",
        ids
    ).fetchall()
    return [r[0] for r in rows]
