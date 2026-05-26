"""
SQLite Memory Store — Vulnerable Memory Assistant Lab

A deliberately insecure memory store that:
  - Has NO user isolation (anyone can read anyone's memories)
  - Has NO content validation (arbitrary content can be stored)
  - Has NO memory expiry (memories persist forever)
  - Has NO size limits (can be flooded with data)
  - Stores metadata as arbitrary JSON with no schema enforcement
"""

import json
import sqlite3
import time
from pathlib import Path

DB_PATH = str(Path(__file__).parent / "memories.db")


class MemoryStore:
    """SQLite-backed memory store with no access control."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        # VULNERABILITY: No index on user_id — but also no access control,
        # so this doesn't matter (all memories are accessible to everyone)
        conn.commit()
        conn.close()

    def store_memory(
        self,
        user_id: str,
        content: str,
        metadata: dict | None = None,
    ) -> int:
        """
        Store a new memory.

        VULNERABILITIES:
        - No content validation or sanitisation
        - No size limit on content
        - No rate limiting
        - metadata is arbitrary JSON — can contain anything
        """
        now = time.time()
        metadata_json = json.dumps(metadata) if metadata else None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "INSERT INTO memories (user_id, content, metadata, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, content, metadata_json, now, now),
        )
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return memory_id

    def get_all_memories(self) -> list[dict]:
        """
        Return ALL memories from ALL users.

        VULNERABILITY: No user filtering — this is a data-leak goldmine.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, user_id, content, metadata, created_at FROM memories "
            "ORDER BY created_at DESC"
        ).fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def get_user_memories(self, user_id: str) -> list[dict]:
        """Return memories for a specific user."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, user_id, content, metadata, created_at FROM memories "
            "WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def search_memories(
        self,
        query: str,
        user_id: str | None = None,
    ) -> list[dict]:
        """
        Simple text search across memories.

        VULNERABILITY: If user_id is None, searches ALL users' memories.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        if user_id:
            rows = conn.execute(
                "SELECT id, user_id, content, metadata, created_at FROM memories "
                "WHERE user_id = ? AND content LIKE ? ORDER BY created_at DESC",
                (user_id, f"%{query}%"),
            ).fetchall()
        else:
            # VULNERABILITY: No user filtering
            rows = conn.execute(
                "SELECT id, user_id, content, metadata, created_at FROM memories "
                "WHERE content LIKE ? ORDER BY created_at DESC",
                (f"%{query}%",),
            ).fetchall()

        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a memory by ID.

        VULNERABILITY: No authorisation check — any user can delete any memory.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,),
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def count_memories(self, user_id: str | None = None) -> int:
        """Count total memories (optionally for a specific user)."""
        conn = sqlite3.connect(self.db_path)
        if user_id:
            row = conn.execute(
                "SELECT COUNT(*) FROM memories WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) FROM memories").fetchone()
        conn.close()
        return row[0]

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict:
        metadata = None
        if row["metadata"]:
            try:
                metadata = json.loads(row["metadata"])
            except json.JSONDecodeError:
                metadata = row["metadata"]

        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "content": row["content"],
            "metadata": metadata,
            "created_at": row["created_at"],
        }
