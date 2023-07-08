import requests
import regex
import datetime

def get_time():

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
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

    response = requests.get('https://meteoinfo.ru/hmc-output/nowcast3/nowcast.php', headers=headers)
    tm0 = regex.findall('([0-9-:.ZT]{2,}?)[,<]', response.text)#время из ответа
    tm = [i.replace(':', '%3A') for i in tm0]# форматируем для url запроса
    dates = [(datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ'))  for i in tm0]# в объект datetime
    timestamps = [str((i - datetime.datetime(1970, 1, 1)).total_seconds()) for i in dates]# в милисекунды
    ts = [i[:-2]+'000' for i in timestamps]# форматируем для url запроса
    timelist = [(i  + datetime.timedelta(hours=3)).strftime('%H:%M') for i in dates]#список доступного времени прогноза(Москва час.пояс)
    print('timelist = ',timelist)
    return tm,ts,timelist
#get_time()
