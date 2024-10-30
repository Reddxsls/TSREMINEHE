import configparser
import os
import sys

import disneynowdl
import pbskidsdl


def get_shows(config_show_list):
    shows_to_download = []

    for key in config_show_list:
        if config_show_list[key] == '1':
            shows_to_download.append(key)

    return shows_to_download

def download_pbskids(show_list, download_path):
    shows_to_download = get_shows(show_list)
    pkdl = pbskidsdl.PBSKidsDL(download_path=download_path, shows=shows_to_download)
    pkdl.run_download()

def download_disneyjr(show_list, download_path):
    shows_to_download = get_shows(show_list)
    djdl = disneynowdl.DisneyNowDL(download_path=download_path, shows=shows_to_download)
    djdl.run_download()

def main():
    exe_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    config_path = f"{exe_path}/show_downloader.conf"

    config = configparser.ConfigParser()

    config.read(config_path)

    download_path = ""

    if "GENERAL" in config:
        if "download_path" in config["GENERAL"]:
            download_path = config["GENERAL"]["download_path"]

    if "PBSKIDS" in config:
        download_pbskids(config["PBSKIDS"], download_path)

    if "DISNEYJR" in config:
        download_disneyjr(config["DISNEYJR"], download_path)

if __name__ == "__main__":
    main()