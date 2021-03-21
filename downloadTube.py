from pytube import YouTube
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# The ProgressBar widget is used to
# visualize the progress of some task
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import time
from configparser import RawConfigParser
import os

class DownloadWindow(BoxLayout):

    video_type  = None
    previousprogress = 0
    liveprogress = 0


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.info.text = ""

        curfolder = os.path.dirname(os.path.abspath(__file__))
        inifile = os.path.join(curfolder, 'downloadTube.ini')
        config = RawConfigParser()
        res = config.read(inifile)

        self.ids.link_field.text = config.get('init_parameters', 'Link')
        self.ids.path_field.text = config.get('init_parameters', 'Path')

    # on_progress_callback takes 4 parameters.
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        DownloadWindow.liveprogress = (int)(bytes_downloaded / total_size * 100)
        if DownloadWindow.liveprogress > DownloadWindow.previousprogress:
           DownloadWindow.previousprogress = DownloadWindow.liveprogress
           print("Downloading Progress = ", DownloadWindow.liveprogress)


    def proceed(self,*args):
        print("proceed args = ",args)
        # Starts the download process
        self.video_type.download(self.ids.path_field.text)
        self.ids.info.text ='[color=#FF0000] Download Completed Successfully...[/color]'


    def fetch_file(self,*args):
        #try:
        url = self.ids.link_field.text
        video = YouTube(url, on_progress_callback=DownloadWindow.on_progress)
        #except:
        #   print("ERROR. Check your:\n  -connection\n  -url is a YouTube url\n\nTry again.")

        # Get the first video type - usually the best quality.
        self.video_type = video.streams.filter(progressive=True, file_extension="mp4").first()

        # Gets the title of the video
        title = video.title

        # Prepares the file for download
        print("Fetching: {}...".format(title))
        self.ids.info.text ='[color=#FF0000] Fetching: {}...[/color]'.format(title)
        file_size = self.video_type.filesize

        Clock.schedule_once(self.proceed,1)

            
    def download_file(self):

        link = self.ids.link_field
        path = self.ids.path_field

        youTube_link  = link.text
        download_path = path.text
        
        if youTube_link == '' or download_path == '':
            self.ids.info.text ='[color=#FF0000] YouTube Link and/ or Download File Path required[/color]'
        else:
            print("Accessing YouTube Link =" ,youTube_link)
            print("Download Path =",download_path)
            self.ids.info.text ='[color=#FF0000] Accessing YouTube URL [/color]'
            Clock.schedule_once(self.fetch_file,1)
            # Searches for the video and sets up the callback to run the progress indicator.


class DownloadTubeApp(App):
    def build(self):
        return DownloadWindow()

if __name__ == "__main__":
   #start()
   dta =DownloadTubeApp()
   dta.run()