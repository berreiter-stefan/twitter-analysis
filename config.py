"""
Containing static config information for the analysis.
"""

from typing import Dict, Tuple

# structure -> full_name: (party, twitter_handle)
MINISTER_TWITTER_INFO: Dict[str, Tuple[str, str]] = {
    "Volker Wissing": ("fdp", "wissing"),
    "Christian Lindner": ("fdp", "c_lindner"),
    "Karl Lauterbach": ("spd", "Karl_Lauterbach"),
    "Annalena Baerbock": ("gruene", "ABaerbock"),
    "Nancy Faeser": ("spd", "NancyFaeser"),
    "Marco Buschmann": ("fdp", "MarcoBuschmann"),
    "Hubertus Heil": ("spd", "hubertus_heil"),
    "Cem Özdemir": ("gruene", "cem_oezdemir"),
    "Steffi Lemke": ("gruene", "SteffiLemke"),
    "Bettina Stark-Watzinger": ("fdp", "starkwatzinger"),
    "Svenja Schulze": ("spd", "SvenjaSchulze68"),
    "Klara Geywitz": ("spd", "klara_geywitz"),
    "Wolfgang Schmidt": ("spd", "W_Schmidt_"),
}
