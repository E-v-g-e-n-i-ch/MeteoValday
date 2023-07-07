import requests
#import re
import regex
import datetime

def get_time():
    cookies = {
        '_ym_uid': '1657790075107118860',
        '_ym_d': '1679994395',
        '66c548aa3ec10b30907b199d946947a3': '9rhv1e8sgf7gfbdt81hap9vc80',
        'tmr_lvid': '62b9c6719cc914db0869b4ef045afa94',
        'tmr_lvidTS': '1657790075817',
        'SL_G_WPT_TO': 'ru',
        'SL_GWPT_Show_Hide_tmp': '1',
        'SL_wptGlobTipTmp': '1',
        'START_POGODA_P': '5021',
        'stan': '5021',
        'lstan': '1486%2C1624%2C1500%2C5021',
        '_ym_isad': '1',
        'tmr_detect': '1%7C1687612675236',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': '_ym_uid=1657790075107118860; _ym_d=1679994395; 66c548aa3ec10b30907b199d946947a3=9rhv1e8sgf7gfbdt81hap9vc80; tmr_lvid=62b9c6719cc914db0869b4ef045afa94; tmr_lvidTS=1657790075817; SL_G_WPT_TO=ru; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; START_POGODA_P=5021; stan=5021; lstan=1486%2C1624%2C1500%2C5021; _ym_isad=1; tmr_detect=1%7C1687612675236',
        'Referer': 'https://meteoinfo.ru/nowcasting',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    response = requests.get('https://meteoinfo.ru/hmc-output/nowcast3/nowcast.php', headers=headers)#cookies=cookies
    #print(response.content)
    #tm = re.findall('default="([0-9-:.ZT]+?)">',response.text)
    tm0 = regex.findall('([0-9-:.ZT]{2,}?)[,<]', response.text)#время из ответа
    tm = [i.replace(':', '%3A') for i in tm0]# форматируем для url запроса
    #print('tm = ',tm)
    dates = [(datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ'))  for i in tm0]# в объект datetime
    #print('dates = ',dates)
    timestamps = [str((i - datetime.datetime(1970, 1, 1)).total_seconds()) for i in dates]# в милисекунды
    #print('timestamps = ',timestamps)
    ts = [i[:-2]+'000' for i in timestamps]# форматируем для url запроса
    #print('ts = ',ts)
    timelist = [(i  + datetime.timedelta(hours=3)).strftime('%H:%M') for i in dates]#список доступного времени прогноза(Москва час.пояс)
    print('timelist = ',timelist)
    return tm,ts,timelist
#get_time()