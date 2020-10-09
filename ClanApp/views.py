from django.shortcuts import render
from django.shortcuts import redirect
from ClanApp.models import Members
from datetime import datetime
from django.template.defaulttags import register
from django.db import connections
from .oauth import OAuth
from django.http import HttpResponse
import requests
from allauth.socialaccount.models import SocialToken
from tabulate import tabulate
from decouple import config

TOKEN = config('BOT_TOKEN')


# Create your views here.
def homepage(request):
    # conn = MySQLdb.connect(user=config('DB_user'), password=config('DB_password'),
    #                        host=config('DB_HOST'),
    #                        database=config('DB_name'), charset='utf8')
    guilds = None
    if request.user.is_authenticated:
        token = SocialToken.objects.get(account__user=request.user)
        headers = {'Authorization': f'Bearer {token}',  # {OAuth.get_access_token(request.GET["code"])}
                   'Content-Type': 'application/json', }
        guilds = requests.get('https://discord.com/api/users/@me/guilds', headers=headers).json()

    try:
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute("SELECT nickname,real_name, DATE_FORMAT(birthday, '%d-%m-%Y'), "
                       "FORMAT((DATE_FORMAT(now(), '%Y')-DATE_FORMAT(birthday, '%Y'))-"
                       "(DATE_FORMAT(now(), '%m-%d')<DATE_FORMAT(birthday, '%m-%d')), 0), "
                       "country, vacation FROM members WHERE vacation='Нет' ORDER BY vacation ASC, id")
        main_table = cursor.fetchall()
        main_table = [list(_) for _ in main_table]
        for member in main_table:
            if None in member:
                cursor.execute("SELECT nickname,real_name, DATE_FORMAT('%d-%m-%Y', FROM_UNIXTIME(birthday/1000)), "
                               "(DATE_FORMAT('%Y','now')-DATE_FORMAT('%Y', FROM_UNIXTIME(birthday/1000)))-"
                               "(DATE_FORMAT('%m-%d','now')<DATE_FORMAT('%m-%d',FROM_UNIXTIME(birthday/1000))), "
                               f"country, vacation FROM members WHERE vacation='Нет' and nickname='{member[0]}'")
                temp = cursor.fetchall()
                index = main_table.index(member)
                main_table[index] = temp[0]

        cursor.execute("SELECT nickname,real_name, DATE_FORMAT(birthday, '%d-%m-%Y'), "
                       "FORMAT((DATE_FORMAT(now(), '%Y')-DATE_FORMAT(birthday, '%Y'))-"
                       "(DATE_FORMAT(now(), '%m-%d')<DATE_FORMAT(birthday, '%m-%d')), 0), "
                       "country, vacation FROM members WHERE vacation!='Нет' ORDER BY vacation ASC, id")
        vac_table = [list(_) for _ in cursor.fetchall()]
        for member in vac_table:
            if None in member:
                cursor.execute("SELECT nickname,real_name, DATE_FORMAT('%d-%m-%Y', FROM_UNIXTIME(birthday/1000)), "
                               "(DATE_FORMAT('%Y','now')-DATE_FORMAT('%Y', FROM_UNIXTIME(birthday/1000)))-"
                               "(DATE_FORMAT('%m-%d','now')<DATE_FORMAT('%m-%d',FROM_UNIXTIME(birthday/1000))), "
                               f"country, vacation FROM members WHERE vacation!='Нет' and nickname='{member[0]}'")
                temp = cursor.fetchall()
                index = vac_table.index(member)
                vac_table[index] = temp[0]
    finally:
        conn.close()
    return render(request=request, template_name="main.html",
                  context={'main_table': main_table, 'vac_table': vac_table, 'guilds': guilds})


def save(request):
    bday = request.POST['birthday']
    nick = request.POST['nickname']
    name = request.POST['name']
    country = request.POST['country']
    vacation = request.POST['vacation']

    date = datetime.strptime(bday, '%Y-%m-%d')  # .strftime('%d-%m-%Y %H:%M:%S')

    Members.objects.using('default').filter(nickname=nick).update(birthday=date, vacation=vacation, real_name=name,
                                                                  country=country)
    update_table()
    return redirect('/')


def delete(request):
    nick = request.POST['nickname']
    Members.objects.using('default').filter(nickname=nick).delete()
    return redirect('/')


def message(request):
    guilds = None
    if request.user.is_authenticated:
        token = SocialToken.objects.get(account__user=request.user)
        headers = {'Authorization': f'Bearer {token}',
                   'Content-Type': 'application/json', }
        guilds = requests.get('https://discord.com/api/users/@me/guilds', headers=headers).json()
    bot = {
        'Authorization': f'Bot {TOKEN}',
    }
    channel_list = {'660797576362328066': None, '660800271965880331': None, '660808504646303744': None}
    for channel_id in channel_list:
        channel_list[channel_id] = requests.get(f'https://discord.com/api/channels/{channel_id}',
                                                headers=bot).json()
    return render(request=request, template_name="message.html",
                  context={'guilds': guilds, 'channels': channel_list.values()})


def send(request):
    bot = {
        'Authorization': f'Bot {TOKEN}',
        'Content-Type': 'application/json',
    }
    channel_id = request.POST['channel']
    text = request.POST['content']
    print(text)
    content = {
        "content": text,
        "tts": False,
    }
    import json
    from websocket import create_connection
    gate = requests.get("https://discord.com/api/gateway/bot", headers=bot).json()['url']
    ws = create_connection(f"{gate}/?v=6&encoding=json")
    ws.send(json.dumps({"op": 2,  # Identify
                        "d": {
                            "token": TOKEN,
                            "properties": {"$os": "windows",
                                           "$browser": "chrome",
                                           "$device": "chrome"},
                            "large_threshold": 250,
                        }}
                       ))
    req = requests.post(f'https://discord.com/api/channels/{channel_id}/messages',
                        headers=bot, json=content)
    ws.close()
    return redirect('/message')


def profile(request):
    token = SocialToken.objects.get(account__user=request.user)
    headers = {
        'Authorization': f'Bearer {token}',  # {OAuth.get_access_token(request.GET["code"])}
        'Content-Type': 'application/json',
    }
    return HttpResponse('123')


def update_table():
    bot = {
        'Authorization': f'Bot {TOKEN}',
    }
    channel_id = 660799528856715300
    # guilds = requests.get('https://discord.com/api/users/@me/guilds', headers=headers)
    # guilds = requests.patch(f'https://discord.com/api/channels/{channel_id}/messages/{main_message_id}',
    #                         headers=bot, json={'content': 'fff'})
    conn = connections['default']
    cursor = conn.cursor()
    # main_table------------------------------------------------------------------------
    main_message_id = 739440611731439697
    cursor.execute("SELECT nickname,real_name, DATE_FORMAT(birthday, '%d-%m-%Y'), "
                   "FORMAT((DATE_FORMAT(now(), '%Y')-DATE_FORMAT(birthday, '%Y'))-"
                   "(DATE_FORMAT(now(), '%m-%d')<DATE_FORMAT(birthday, '%m-%d')), 0), "
                   "country, vacation FROM members WHERE vacation='Нет' ORDER BY vacation ASC, id")
    rows = cursor.fetchall()
    rows = [list(_) for _ in rows]
    table = []
    for row in rows:
        table.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    content = '@everyone\n' + '```css\n' + tabulate(table, headers=['NICKNAME', 'NAME', 'BIRTHDAY', 'AGE', 'COUNTRY',
                                                                    'VACATION'], tablefmt="simple",
                                                    showindex=[x + 1 for x in range(len(table))]) + '``` '
    requests.patch(f'https://discord.com/api/channels/{channel_id}/messages/{main_message_id}',
                   headers=bot, json={'content': content})
    # vac_table--------------------------------------------------------------------------
    vac_message_id = 739440690391679017
    len_main_table = len(table)
    table.clear()
    cursor.execute("SELECT nickname,real_name, DATE_FORMAT(birthday, '%d-%m-%Y'), "
                   "FORMAT((DATE_FORMAT(now(), '%Y')-DATE_FORMAT(birthday, '%Y'))-"
                   "(DATE_FORMAT(now(), '%m-%d')<DATE_FORMAT(birthday, '%m-%d')), 0), "
                   "country, vacation FROM members WHERE vacation!='Нет' ORDER BY vacation ASC, id")
    vac_rows = cursor.fetchall()
    vac_rows = [list(_) for _ in vac_rows]
    for row in vac_rows:
        table.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    content = '```css\n' + tabulate(table, headers=['NICKNAME', 'NAME', 'BIRTHDAY', 'AGE', 'COUNTRY', 'VACATION'],
                                    tablefmt="simple",
                                    showindex=[x + len_main_table + 1 for x in range(len(table))]) + '```' + '@everyone'
    requests.patch(f'https://discord.com/api/channels/{channel_id}/messages/{vac_message_id}',
                   headers=bot, json={'content': content})
    conn.close()


@register.filter
def get_range(value):
    return range(len(value))
