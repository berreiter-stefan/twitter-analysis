"""
Includes utility functions to export data to other formats
"""
from csv import DictWriter
from typing import List, Dict, Any


def export_container_to_csv(container: List[Dict[str, Any]], path: str) -> None:
    """saves the data into the /data folder."""
    keys = container[0].keys()
    with open(path, "w", newline="", encoding="utf") as output_file:
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(container)
