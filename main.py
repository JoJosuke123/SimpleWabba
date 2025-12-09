"""
Entry point for the program.
Downloads files listed in a Wabbajack modlist.
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from camoufox.sync_api import Camoufox
from camoufox import DefaultAddons
from playwright.sync_api import Page

from modules import hashing, online, wabbajack_reader


def download_full_modlist(wabbajack_path: Path, download_dir: Path) -> None:
    """
    Main function to download files from Wabbajack modlist.

    Args:
        wabbajack_path: Path to the Wabbajack modlist file.
        download_dir: Path to the directory where files will be downloaded
    """

    # Parse Wabbajack modlist
    modlist_data: list[tuple[str, int, str, int, int]] = wabbajack_reader.parse_modlist(wabbajack_path)
    n_mods: int = len(modlist_data)
    print(f"Found {n_mods} files to download.")

    # Open browser using saved login state
    # Disable uBlock Origin to enable faster downloads
    with Camoufox(headless = True, persistent_context = True, user_data_dir = online.CONTEXT_DIR, exclude_addons = [DefaultAddons.UBO]) as browser:
        page: Page = browser.new_page()

        # Download each file
        file_name: str
        file_size: int
        hash_code: str
        game_id: int
        file_id: int
        for i, (file_name, file_size, hash_code, game_id, file_id) in enumerate(modlist_data, start = 1):
            print(f"Processing file {i}/{n_mods}.")
            
            # File destination
            output_path: Path = download_dir / file_name

            # Check if file already exists
            # NOTE: This only checks for file size, not hash. Hash check may be skipped if the program is closed during hash calculation.
            if output_path.is_file() and output_path.stat().st_size == file_size:
                print(f"Skipping {file_name}, already downloaded.")
                continue

            print(f"Downloading {file_name}...")

            # Download the file
            correctly_downloaded: bool = False
            url: str = online.get_direct_url(page, file_id, game_id)
            while not correctly_downloaded:

                online.direct_download(url, output_path)

                # Verify the hash
                correctly_downloaded = hashing.compare_hash(output_path, hash_code)
                if not correctly_downloaded:
                    output_path.unlink()
                    print(f"Hash mismatch for {file_name}, re-downloading...")
    
    print("All files downloaded successfully.")

if __name__ == '__main__':

    # Parse command-line arguments
    parser: ArgumentParser = ArgumentParser(description = "Download files from a Wabbajack modlist.")
    parser.add_argument('wabbajack_path', type = Path, help = "Path to the Wabbajack modlist file (.wabbajack).")
    parser.add_argument('--download-dir', type = Path, default = Path('downloaded_mods'), help = "Directory to download files to. Default is 'downloaded_mods'.")
    parser.add_argument('--login', action = 'store_true', help = "Login to Nexus Mods, even if a saved login state exists.")
    args: Namespace = parser.parse_args()

    # Login if requested
    if args.login:
        online.login()
        print("Login state saved.")
    
    # Start main download process
    download_full_modlist(args.wabbajack_path, args.download_dir)

