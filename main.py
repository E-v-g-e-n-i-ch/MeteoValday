from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from bs4 import BeautifulSoup
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import certifi
from time_now import get_time
from kivy_garden_tms.mapview import MapView
import shutil

from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty

def clear_cache():
    shutil.rmtree('MVcache', ignore_errors=True)

Builder.load_file('meteograms.kv')
Builder.load_file('radar.kv')
Builder.load_file('main.kv')
Builder.load_file('about.kv')

def get_url_images(url):
    urls = [
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/14-%D0%B4%D0%BD%D0%B5%D0%B9/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301',
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/%D0%BF%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7/multimodel/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301?fcstlength=168&params%5B%5D=&params%5B%5D=NMM22&params%5B%5D=NEMS12&params%5B%5D=NEMS12_E&params%5B%5D=NEMSGLOBAL&params%5B%5D=NEMSGLOBAL_E&params%5B%5D=&params%5B%5D=IFS04&params%5B%5D=UMGLOBAL10&params%5B%5D=ICONEU&params%5B%5D=ICON&params%5B%5D=GFS05&params%5B%5D=GEM15&params%5B%5D=MFEU&params%5B%5D=MFGLOBAL',
        'https://www.meteoblue.com/ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0/%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8F/%D0%92%D0%B0%D0%BB%D0%B4%D0%B0%D0%B9_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F_477301?day=1'
    ]
    headers = {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain'}
    r = UrlRequest(urls[url], req_headers=headers, ca_file=certifi.where(), on_redirect=True, cookies='speed=METER_PER_SECOND',timeout=15)
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


class MeteogramScreen(Screen):
    pass

class RadarScreen(Screen):
    pass

class TitleScreen(Screen):
    pass

class Podlozhka(MapView):
    pass

class NowcastMap(MapView):
    pass
    
class Vybor(Screen):
    pass
    
class Radarinfo(Screen):
    pass
    
class Meteograminfo(Screen):
    pass
    
class AppInfo(Screen):
    pass
    
class InfoScreen(ScreenManager):
    pass
    
class ErrorScreen(Screen):
    pass

class MultiApp(App):
    def on_pause(self): # чтобы не висело приложение в процессах, а завершалось при выходе
        return False
    clear_cache()
    tm, ts, dt = get_time()
    def build(self):
        self.icon = 'iconka.png'
        self.root_layout = TitleScreen()
        return  self.root_layout
    def meteogram(self):
        try:
            self.source1 = get_url_images(2) 
            self.source2 = get_url_images(0)
            self.source3 = get_url_images(1)
            self.root_layout.clear_widgets()
            self.root_layout.add_widget(MeteogramScreen())
        except Exception:                            # если сервер долго не отвечает
            print('meteoblue.com -> timeout -> out') # переход на ErrorScreen
            self.root_layout.clear_widgets()
            self.root_layout.add_widget(ErrorScreen())
    def out(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(TitleScreen())
    def radar(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(RadarScreen())
    def info(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(InfoScreen())
    def __init__(self, **kwargs):
        super(MultiApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.back_key)

    def back_key(self, window, key, *args): # фунция обрабатывающая кнопку "назад" на андроид
        if key == 27 :                       # или "esc" на десктопе
            if self.root_layout.children[0].name not in ['MainScreen','MainBoxlayout']:
                print((self.root_layout.children[0].name))
                if self.root_layout.children[0].name == 'InfoScreen' and self.root_layout.children[0].current != 'vybor':
                    print("self.root_layout.children[0].name == 'InfoScreen'")
                    print(self.root_layout.children[0].current)
                    self.root_layout.clear_widgets()
                    self.root_layout.add_widget(InfoScreen())
                else:
                    self.root_layout.clear_widgets()
                    self.root_layout.add_widget(TitleScreen())
                return True
            else:
                return False


MultiApp().run()
