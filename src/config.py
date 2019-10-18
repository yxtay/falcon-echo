import os
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path


def read_config(ini_file="app.ini"):
    # read configs
    ini_path = Path("configs", ini_file)
    parser = ConfigParser()
    parser.read([ini_path])
    # environment config
    environment = os.environ.get("ENVIRONMENT", "dev")
    config = parser[environment]
    return config


CONFIG = read_config()

APP_NAME = CONFIG["APP_NAME"]
GCP_PROJECT = CONFIG["GCP_PROJECT"]
LOGGING_FILE = CONFIG["LOGGING_FILE"]
LOGGING_CONSOLE = CONFIG.getboolean("LOGGING_CONSOLE")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("key", help="key name to get value")
    args = parser.parse_args()
    print(CONFIG[args.key])
