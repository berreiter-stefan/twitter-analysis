"""
Includes utility functions to export data to other formats
"""
from csv import DictWriter
from typing import List, Dict, Any


def export_container_to_csv(container: List[Dict[str, Any]], path: str) -> None:
    """saves the data into the /data folder.

    Parameters
    ----------
    container: List[Dict[str, Any]] :
        the data container (a list of dictionaries) which needs to be written to disc

    path: str :
        the relative filepath you want to write the output to.


    Returns
    -------
    None
    """
    keys = container[0].keys()
    with open(path, "w", newline="", encoding="utf") as output_file:
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(container)
