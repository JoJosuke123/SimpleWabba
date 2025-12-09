"""
Module to handle online interactions with Nexus Mods.

Useful constants:
    CONTEXT_DIR: Directory to save browser context (login state). To be used with Playwright/Camoufox persistent contexts.

Useful functions:
    login
    get_direct_url
    direct_download
"""

from pathlib import Path
import subprocess
from typing import Literal
import urllib.parse

from camoufox.sync_api import Camoufox
from playwright.sync_api import Page


# Constants
CONTEXT_DIR: Path = Path('context') # Directory to save browser context (login state)


def login() -> None:
    """
    Login to Nexus Mods and save the authentication state and save it to CONTEXT_DIR for future use with peristent contexts.
    """

    # Launch browser for manual login and save context
    with Camoufox(headless = False, persistent_context = True, user_data_dir = CONTEXT_DIR) as browser:
        page: Page = browser.new_page()
        page.goto('https://www.nexusmods.com/') # Homepage

        # Wait for user to login manually
        input("Press Enter after logging in...")

def get_direct_url(page: Page, file_id: int, game_id: int) -> str:
    """
    Get the direct download URL for a file.

    Args:
        page: The Playwright page object
        file_id: The file ID
        game_id: The game ID
    """

    # Go to Nexus Mods and update ad-related cookies if needed
    vortex_url: str = 'https://www.nexusmods.com/site/mods/1'   # any other mod page would work
    if not page.url == vortex_url:
        page.goto(vortex_url)

    # Get the download URL via the API
    get_url_js: str = """
        async (dataBody) => {
            const response = await fetch(
                "https://www.nexusmods.com/Core/Libs/Common/Managers/Downloads?GenerateDownloadUrl",
                {
                    method: "POST",
                    headers: {
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                body: dataBody
                }
            );
            return await response.json();
        }
    """
    result: dict[Literal['url'], str] = page.evaluate(get_url_js, f'fid={file_id}&game_id={game_id}')
    url: str = result['url']

    # Encode the URL properly
    return urllib.parse.quote(url, safe = ':/?&=%')

def direct_download(url: str, output_path: Path) -> None:
    """
    Download a file from a direct URL.

    Args:
        url: The direct download URL
        output_path: The path to save the downloaded file
    """

    # Prepare curl command
    cmd_args: list[str] = ['curl', '-L', '-o', str(output_path), '--create-dirs', '--progress-bar']

    # Resume download if file exists
    if output_path.is_file():
        cmd_args.extend(['-C', '-'])

    # Add the URL and execute the command
    cmd_args.append(url)
    subprocess.run(cmd_args, check = True)
