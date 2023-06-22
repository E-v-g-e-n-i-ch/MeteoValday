from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from bs4 import BeautifulSoup
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import certifi


def get_url_images(url):
    urls = [
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/14-%D0%B4%D0%BD%D0%B5%D0%B9/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301',
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/%D0%BF%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7/multimodel/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301?fcstlength=168&params%5B%5D=&params%5B%5D=NMM22&params%5B%5D=NEMS12&params%5B%5D=NEMS12_E&params%5B%5D=NEMSGLOBAL&params%5B%5D=NEMSGLOBAL_E&params%5B%5D=&params%5B%5D=IFS04&params%5B%5D=UMGLOBAL10&params%5B%5D=ICONEU&params%5B%5D=ICON&params%5B%5D=GFS05&params%5B%5D=GEM15&params%5B%5D=MFEU&params%5B%5D=MFGLOBAL',
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8F/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301?day=1'
    ]
    headers = {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain'}
    r = UrlRequest(urls[url], req_headers=headers, ca_file=certifi.where(), on_redirect=True, cookies='speed=METER_PER_SECOND')
    Clock.start_clock()
    while not r.is_finished:  # start while loop to test is_finished
        Clock.tick()
    Clock.stop_clock()
    soup = BeautifulSoup(r.result)
    if url == 1 or url == 2:
        ssylka = 'https:' + soup.find('img', alt="meteoblue")['data-original']
    else:
        ssylka = 'https:' + soup.find('a',id="chart_download")['href']
    return ssylka


class ReadWriteScreen(Screen):
    source1 = StringProperty()
    source2 = StringProperty()
    source3 = StringProperty()

    def on_pre_enter(self,  *args):
        if self.source1 == '':
            self.source1 = get_url_images(2)
        if self.source2 == '':
            self.source2 = get_url_images(0)
        if self.source3 == '':
            self.source3 = get_url_images(1)

class TitleScreen(Screen):
    source_down = 'Images/down.png'

class InfoScreen(Screen):
    pass

class MeteoValdayApp(App):
    def on_pause(self): # чтобы не висело приложение в процессах, а завершалось при выходе
        return False
    def build(self):
        self.icon = 'iconka.png'
        return Builder.load_file('kivy.kv')


MeteoValdayApp().run()
