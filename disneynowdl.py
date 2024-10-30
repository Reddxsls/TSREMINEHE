import sys
import requests, urllib
import pathlib
import pickle
import yt_dlp

from html.parser import HTMLParser

def main():
    shows = [
        "doc-mcstuffins",
    ]

    djdl = DisneyNowDL(shows=shows)
    djdl.run_download()

class DisneyHTMLParser(HTMLParser):
    lsOpenTags = list()

    isTileList = False
    isTileTitle = False
    section_title = ""

    currHref = ""
    currTitle = ""
    show = ""

    download_path = ""
    already_downloaded = {}

    def populate_params(self, show, download_path, already_downloaded):
        self.show = show
        self.already_downloaded = already_downloaded
        self.download_path = download_path

    def handle_starttag(self, tag, attrs):
        toDownload = True
        if tag == 'div':
            for attr in attrs:
                if "class" in attr[0] and "tilegroup__title" in attr[1]:
                    self.isTileTitle = True
                    return
                elif "class" in attr[0] and "tilegroup__list" in attr[1]:
                    self.isTileList = True
                    return

        elif tag == 'a' and len(self.section_title) != 0:
            for attr in attrs:
                if "href" in attr[0]:
                    self.currHref = attr[1]
                elif "title" in attr[0]:
                    self.currTitle = attr[1]

            if len(self.currTitle) ==  0 or len(self.currHref) == 0:
                toDownload = False

            if len(self.currTitle) > 0 and self.currTitle in self.already_downloaded[self.show]:
                toDownload = False


        if len(self.currHref) > 0 and tag == 'span':
            for attr in attrs:
                if "class" in attr[0] and "icon-lock" in attr[1]:
                    toDownload = False
        
        if not toDownload:
            self.currHref = ""
            self.currTitle = ""

            
    def handle_data(self, data):
        if self.isTileTitle:
            self.section_title = data
            pathlib.Path(self.download_path + "/" + self.section_title).mkdir(parents=True, exist_ok=True)
            self.isTileTitle = False


    def handle_endtag(self, tag):
        if tag == "a":
            if len(self.currHref) == 0 or len(self.currTitle) == 0 or len(self.section_title) == 0:
                return

            if self.section_title.lower() == 'games':
                return

            try:
                ydl_opts = {
                    'outtmpl': self.download_path + "/" + self.section_title + u'/%(title)s.%(ext)s',
                    'format': '[tbr<=2199]',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://disneynow.com{self.currHref}"])

                self.already_downloaded[self.show].append(self.currTitle)
            except:
                print(f"----- ERROR: Couldn't yt-dlp, show: {self.show}, section: {self.section_title}, https://disneynow.com{self.currHref}")


    def get_already_downloaded(self):
        return self.already_downloaded


class DisneyNowDL:
    url_base = "https://disneynow.com/shows/"
    download_path = str(pathlib.Path.home()) + "/Downloads/TV_Shows/"

    already_downloaded = {}
    curr_downpath = ""
    already_downloaded_file = ""

    def __init__(self, download_path="", shows=[]):
        if len(download_path) > 0:
            self.download_path = download_path
        if len(shows) > 0:
            self.shows = shows

        self.already_downloaded_file = f"{self.download_path}.disneydownlist"

        pathlib.Path(self.download_path).mkdir(parents=True, exist_ok=True)

        self.populate_downloaded_list()

    def populate_downloaded_list(self):
        try:
            with open(self.already_downloaded_file, 'rb') as filehandle:
                self.already_downloaded = pickle.load(filehandle)
        except:
            pass

    def write_downloaded_list(self):
        with open(self.already_downloaded_file, 'wb') as filehandle:
            pickle.dump(self.already_downloaded, filehandle)

    def remove_episode_from_list(self, show, episode):
        if show in self.already_downloaded.keys():
            if episode in self.already_downloaded[show]:
                self.already_downloaded[show].remove(episode)
        self.write_downloaded_list()

    def run_download(self):
        for show in self.shows:
            print(show)

            if show not in self.already_downloaded:
                self.already_downloaded[show] = []

            curr_downpath = f"{self.download_path}{show}"
            pathlib.Path(curr_downpath).mkdir(parents=True, exist_ok=True)

            url = f"{self.url_base}{show}"
            try:
                disney_html = str(urllib.request.urlopen(url).read())

                parser = DisneyHTMLParser()
                parser.populate_params(show, curr_downpath, self.already_downloaded)
                parser.feed(disney_html)
                self.already_downloaded = parser.get_already_downloaded()

                self.write_downloaded_list()
            except:
                with open('show_download.error', 'a') as errorlog:
                    errorlog.write(f"Problem with: {url}\n")

if __name__ == "__main__":
    main()