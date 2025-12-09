# SimpleWabba

A simple way to download Wabbajack modlists directly from NexusMods.

## Features

- **Simple** command-line interface.
- Runs in the **background**.
- **No 5-second delay** per mod.
- **Maximum download speed** available without premium.

## Getting Started

- Install Dependencies

    ````sh
    pip install -r requirements.txt
    ````

- Follow the instruction to [download the browser for Camoufox](https://camoufox.com/python/installation/#download-the-browser).  
*Don't worry: you only need to copy-and-paste one or two lines.*

- You're ready to start downloading modlists!

## Usage

You must specify the path to your `.wabbajack` modlist file.  
Find it at `path_to_wabbajack/version/downloaded_mod_lists/xxx.wabbajack`.

### Command Line Options

- `--login`  
Log in to Nexus Mods (required only for first use).
- `--download-dir <directory>`  
Directory where mods will be downloaded (optional: defaults to `downloaded_mods`).

### Example

````sh
python main.py path/to/modlist.wabbajack --download-dir path/to/download --login
````

## Additional Notes

- Don't worry about the errors you get after interrupting the program, they are harmless.

---

*SimpleWabba is designed for simplicity and ease of debugging.*
