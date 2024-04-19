"""Coargus's Download utilities."""

import logging
import subprocess
from pathlib import Path

import gdown

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_file_from_google_drive(
    gdrive_url: str, destination_path: str
) -> bool:
    """Downloads a file from Google Drive given a sharing link and saves it to a specified path.

    Parameters:
    gdrive_url (str): The Google Drive file sharing URL.
    destination_path (str): The path and filename where the file will be saved.

    Returns:
    bool: True if the download was successful, False otherwise.
    """  # noqa: E501
    destination_path = Path(destination_path)

    try:
        # Validate URL
        if "drive.google.com" not in gdrive_url:
            logging.error("Invalid Google Drive URL.")
            return False

        # Extract the file ID from the URL
        start = gdrive_url.find("/d/") + 3
        end = gdrive_url.find("/view")
        if "view" in gdrive_url:
            if start == -1 or end == -1 or start > end:
                logging.error("Could not parse the Google Drive URL.")
                return False
            file_id = gdrive_url[start:end]
        else:
            file_id = gdrive_url[start:].split("/")[0]

        # Construct the download URL
        download_url = f"https://drive.google.com/uc?id={file_id}"

        # Check if the destination directory exists, create if it doesn't
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        # Download the file
        gdown.download(download_url, str(destination_path), quiet=False)
        logging.info(f"File downloaded successfully: {destination_path}")  # noqa: G004

    except Exception:
        logging.exception("Failed to download the file.")
        return False

    else:
        return True


def download_folder_from_google_drive(
    gdrive_url: str, destination_path: str
) -> bool:
    """Downloads a folder from Google Drive given a sharing link and saves it to a specified path.

    Parameters:
    gdrive_url (str): The Google Drive folder sharing URL.
    destination_path (str): The path where the folder will be saved.

    Returns:
    bool: True if the download was successful, False otherwise.
    """  # noqa: E501
    try:
        # Validate URL
        if "drive.google.com" not in gdrive_url:
            logging.error("Invalid Google Drive URL.")
            return False

        # Clean URL from any unnecessary suffix
        if gdrive_url.endswith("?usp=sharing"):
            gdrive_url = gdrive_url[: -len("?usp=sharing")]

        # Prepare the destination path
        destination_path = Path(destination_path)
        destination_path.mkdir(parents=True, exist_ok=True)

        # Execute gdown command
        cmd = f"gdown --fuzzy '{gdrive_url}' -O '{destination_path}' --folder"
        subprocess.run(cmd, shell=True, check=True)  # noqa: S602
        logging.info(
            f"Folder downloaded successfully: {destination_path}"  # noqa: G004
        )

    except subprocess.CalledProcessError:
        logging.exception("Failed to download the folder.")
        return False

    except Exception:
        logging.exception("Unexpected error occurred.")
        return False

    return True
