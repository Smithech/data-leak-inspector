"""
SQLite implementation of the scan repository.
"""

import json
import sqlite3
from datetime import datetime

from leak_inspector.application.ports.scan_repository import ScanRepository
from leak_inspector.domain.models import ScanResult


class SQLiteScanRepository(ScanRepository):
    """
    SQLite-based repository for storing scan results.
    """

    def __init__(self, db_path: str = "dli.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS scan_results (
            file_id TEXT NOT NULL,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            modified_time TEXT NOT NULL,
            mode TEXT NOT NULL,
            exposure_level TEXT,
            risk_level TEXT,
            pii_summary TEXT,
            
            PRIMARY KEY (source, file_id, modified_time)
        )
        """

        self.conn.execute(query)
        self.conn.commit()

    def is_scanned(self, source: str, file_id: str, modified_time: datetime) -> bool:
        query = """
        SELECT 1 FROM scan_results
        WHERE source = ? AND file_id = ? AND modified_time = ?
        LIMIT 1
        """

        cursor = self.conn.execute(
            query,
            (source, file_id, modified_time.isoformat()),
        )

        return cursor.fetchone() is not None

    def save(self, result: ScanResult) -> None:
        query = """
        INSERT INTO scan_results (
            file_id,
            name,
            source,
            modified_time,
            mode,
            exposure_level,
            risk_level,
            pii_summary            
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.conn.execute(
            query,
            (
                result.file_id,
                result.name,
                result.source,
                result.modified_time.isoformat(),
                result.mode,
                result.exposure_level,
                result.risk_level.value,                
                json.dumps(result.pii_summary.model_dump(exclude_none=True)),
                
            ),
        )

        self.conn.commit()
