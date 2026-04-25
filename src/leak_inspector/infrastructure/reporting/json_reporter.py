"""
JSON reporter implementation.
"""

import json
from pathlib import Path
from typing import Iterable

from leak_inspector.domain.models import ScanResult
from leak_inspector.domain.reporting import Reporter


class JsonReporter(Reporter):
    """
    Export scan results as JSON.
    """

    def generate(self, results: Iterable[ScanResult], output: Path) -> None:

        results_list = list(results)

        data = {
            "files_scanned": len(results_list),
            "results": [
                {
                    "file_id": r.file_id,
                    "modified_time": r.modified_time.isoformat(),
                    "risk_level": r.risk_level.value,
                    "pii_summary": r.pii_summary.model_dump(),
                }
                for r in results_list
            ],
        }

        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
