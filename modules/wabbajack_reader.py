"""
Module for reading and parsing Wabbajack modlist files.

Useful functions:
    parse_modlist
"""

import json
from pathlib import Path
from typing import Any
import zipfile


# Constants
GAME_IDS_JSON: Path = Path('game_ids.json')


def wabbajack2list(wabbajack_file: Path) -> list[dict[str, Any]]:
    """
    Reads the modlist from a Wabbajack file and returns it unprocessed as a list of dictionaries.

    Args:
        wabbajack_file: The path to the .wabbajack file.
    """
    
    with zipfile.ZipFile(wabbajack_file, 'r') as wabbajack_zip:
        with wabbajack_zip.open('modlist') as file:
            modlist: bytes = file.read()
    modlist_json: dict[str, Any] = json.loads(modlist)

    return modlist_json['Archives']

def extract_data(mods_list: list[dict[str, Any]]) -> list[tuple[str, int, str, int, int]]:
    """
    Extracts relevant data from the modlist.

    Args:
        mods_list: The modlist as a list of dictionaries.

    Returns:
        A list of tuples containing (file_name, size, hash_code, game_id, file_id).
    """

    # Load game IDs from JSON file
    with open(GAME_IDS_JSON) as file:
        game_ids_dict: dict[str, int] = json.load(file)
        
    data: list[tuple[str, int, str, int, int]] = []
    for mod_data in mods_list:

        # Only process Nexus Downloader mods
        if mod_data['State']['$type'] != 'NexusDownloader, Wabbajack.Lib':
            continue

        # Extract relevant data
        game_name: str = mod_data['State']['GameName']

        file_name: str = mod_data['Name']
        size: int = mod_data['Size']
        hash_code: str = mod_data['Hash']
        game_id: int = game_ids_dict[game_name]
        file_id: int = mod_data['State']['FileID']

        data.append((file_name, size, hash_code, game_id, file_id))

    return data

def parse_modlist(wabbajack_file: Path) -> list[tuple[str, int, str, int, int]]:
    """
    Parses a Wabbajack modlist file and extracts relevant data.

    Args:
        wabbajack_file: The path to the .wabbajack file.
    
    Returns:
        A list of tuples containing (file_name, size, hash_code, game_id, file_id).
    """

    mods_list: list[dict[str, Any]] = wabbajack2list(wabbajack_file)
    return extract_data(mods_list)
