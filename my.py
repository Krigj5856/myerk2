#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miner Automation for Ubuntu RDP - Terminals 1-150
3 Tabs/Batch | 1 Min Gap | 6 Min Check via Unmineable API
"""

import os
import sys
import subprocess
import time
import argparse
import psutil
import shutil
from datetime import datetime
from typing import Optional

# ==================== AUTO INSTALL DEPENDENCIES ====================
def auto_install_dependencies():
    required = ['requests', 'psutil', 'pillow']
    for package in required:
        try:
            if package == 'pillow':
                __import__('PIL')
            else:
                __import__(package)
            print(f"[OK] {package} already installed")
        except ImportError:
            print(f"[*] Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"[OK] {package} installed")

auto_install_dependencies()

import requests
from PIL import ImageGrab

# ==================== TELEGRAM ====================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8670890083:AAFdQaEiC67jmk6l8jxxdG01NTEN4JxvPUc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6955911349")

class TelegramLogger:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    def send_message(self, message: str):
        try:
            requests.post(f"{self.base_url}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
        except:
            pass
    def send_photo(self, image_path: str, caption: str):
        try:
            with open(image_path, 'rb') as f:
                requests.post(f"{self.base_url}/sendPhoto", files={'photo': f}, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'HTML'}, timeout=30)
            os.remove(image_path)
        except:
            pass

telegram = TelegramLogger()

# ==================== BROWSER DETECTION & INSTALLATION ====================
def check_browser():
    """Check for Firefox or Chrome, install Firefox if none found"""
    
    # Check for Firefox
    firefox_paths = [
        "/usr/bin/firefox",
        "/usr/local/bin/firefox",
        "/snap/bin/firefox"
    ]
    
    for path in firefox_paths:
        if os.path.exists(path):
            print(f"[OK] Firefox found at: {path}")
            return path, "firefox"
    
    # Check for Chrome
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/local/bin/google-chrome",
        "/snap/bin/chromium"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"[OK] Chrome found at: {path}")
            return path, "chrome"
    
    # If no browser found, install Firefox
    print("[*] No browser found. Installing Firefox...")
    try:
        subprocess.check_call(["sudo", "apt", "update", "-qq"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["sudo", "apt", "install", "-y", "firefox"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[OK] Firefox installed successfully")
        return "/usr/bin/firefox", "firefox"
    except Exception as e:
        print(f"[ERROR] Failed to install Firefox: {e}")
        return None, None

def get_browser_command(browser_path: str, browser_type: str, url: str):
    """Get the command to open a new window"""
    if browser_type == "firefox":
        return [browser_path, "-new-window", url]
    else:
        # Chrome/Chromium
        return [browser_path, "--new-window", url]

# ==================== CONFIG ====================
API_BASE = "https://api.unmineable.com/v5"
WALLET_ADDRESS = "nano_1g97x3h6wxd4h577p6dricapigs78ccc7tcowjfm67hewsmg7qob4xwc8jak"
COIN = "NANO"
BATCH_SIZE = 3
GAP_BETWEEN_BATCHES = 60
CHECK_INTERVAL = 360

# ==================== TERMINALS 1-150 ====================
TERMINALS = []

# Terminals 1-30
for i in range(1, 31):
    TERMINALS.append([i, f"Terminal {i}", "", ""])

# Add actual URLs for Terminals 1-30
urls_1_30 = [
    "https://ais-pre-lpa5neewvrg3efhfoqiuc5-158414749269.asia-east1.run.app",
    "https://ais-pre-u27dqik55hsbpuc3a4zdjg-158414749269.asia-east1.run.app",
    "https://ais-pre-s46wg4fbogdnawfz7lponw-158414749269.asia-east1.run.app",
    "https://ais-pre-xnlziqjgwx25kek5dt7vjg-158414749269.asia-east1.run.app",
    "https://ais-pre-fnzsax2ntgpumss2fv7gbs-158414749269.asia-east1.run.app",
    "https://ais-pre-asmthlh2hwe2zc5aucqkux-158414749269.asia-east1.run.app",
    "https://ais-pre-plttdjcx2xfi7ae5fyu6mx-158414749269.asia-east1.run.app",
    "https://ais-pre-l4brlflom366xidrwprvjb-158414749269.asia-east1.run.app",
    "https://ais-pre-kgpcawracefzloi6423wwz-158414749269.asia-east1.run.app",
    "https://ais-pre-yeb5zgkfkptb4g2n7sw35p-158414749269.asia-east1.run.app",
    "https://ais-pre-s4akyhx55nwwsd7eix526w-158414749269.asia-east1.run.app",
    "https://ais-pre-acjdhdwko7xatspy2gsc6j-158414749269.asia-east1.run.app",
    "https://ais-pre-sgqlk63rywltds2oqvgfrk-158414749269.asia-east1.run.app",
    "https://ais-pre-lcfu33gv6j7wq3jvzsmiyk-158414749269.asia-east1.run.app",
    "https://ais-pre-3fggqei6e4uumtzy6pkao6-158414749269.asia-east1.run.app",
    "https://ais-pre-e5rt6ghxcshonxkr3n2po3-158414749269.asia-east1.run.app",
    "https://ais-pre-ag7j6atapmrwbqd24hkmp6-158414749269.asia-east1.run.app",
    "https://ais-pre-oyoftfifg6xqgv4ehkhbpt-158414749269.asia-east1.run.app",
    "https://ais-pre-yuemoooayebljtmf7jlhus-158414749269.asia-east1.run.app",
    "https://ais-pre-af6dupaeexazcqo4rjfoho-158414749269.asia-east1.run.app",
    "https://ais-pre-kg2efziimzs64e3573gx2s-158414749269.asia-east1.run.app",
    "https://ais-pre-hfsvrh2trwclm5qvxyfxsf-158414749269.asia-east1.run.app",
    "https://ais-pre-fikatfynsoebnu65bjwjyv-158414749269.asia-east1.run.app",
    "https://ais-pre-7g6ghr4tgbx4wnzvvl5to2-158414749269.asia-east1.run.app",
    "https://ais-pre-434666jxs4tm7ei52tgsr4-158414749269.asia-east1.run.app",
    "https://ais-pre-wwaaefvpl6lmvrqk3lh6u7-158414749269.asia-east1.run.app",
    "https://ais-pre-22twhibrd5ag2smw4t6iuw-158414749269.asia-east1.run.app",
    "https://ais-pre-wx3rtfealli6p4qcqtxjdd-158414749269.asia-east1.run.app",
    "https://ais-pre-4elhve7u4jvldqq3qhdduo-158414749269.asia-east1.run.app",
    "https://ais-pre-wfwhkeqvy23mf2h5kheouz-158414749269.asia-east1.run.app",
]

# Terminals 31-60
urls_31_60 = [
    "https://ais-pre-l4nexpjplufhhrp3rg2mnr-49332687696.asia-east1.run.app",
    "https://ais-pre-xrgbkmdurfjazearttecfg-49332687696.asia-east1.run.app",
    "https://ais-pre-r7cl5ikxlphlx2jnqfr4n3-49332687696.asia-east1.run.app",
    "https://ais-pre-lmkapxey2y4blw6wv2dt5i-49332687696.asia-east1.run.app",
    "https://ais-pre-ctceihay3r4nctd5gsps7y-49332687696.asia-east1.run.app",
    "https://ais-pre-thtwvzhh6yapos3lglf5z3-49332687696.asia-east1.run.app",
    "https://ais-pre-pupk4rdctuhhkoxcb4ogoj-49332687696.asia-east1.run.app",
    "https://ais-pre-j53c3ev3l7r2bxzxt23kta-49332687696.asia-east1.run.app",
    "https://ais-pre-ozd2yr57dcdy66vn25p6sa-49332687696.asia-east1.run.app",
    "https://ais-pre-6cgwknlc2logtvfnkp5kv4-49332687696.asia-east1.run.app",
    "https://ais-pre-pk4iomeemgbzyjdnrmzbls-49332687696.asia-east1.run.app",
    "https://ais-pre-bi7j3jwv6bys5sukvgnrzs-49332687696.asia-east1.run.app",
    "https://ais-pre-waqj65qludc3ao6mzxkv67-49332687696.asia-east1.run.app",
    "https://ais-pre-7a6bv6o77z65omxcamt3km-49332687696.asia-east1.run.app",
    "https://ais-pre-65645qtry5k6oj4quvle37-49332687696.asia-east1.run.app",
    "https://ais-pre-lkvnsbtsrygnajjz3lwbe3-49332687696.asia-east1.run.app",
    "https://ais-pre-npvl6zxgbscqc37qgqw27c-49332687696.asia-east1.run.app",
    "https://ais-pre-fop7mm76x54b5v2pffflv6-49332687696.asia-east1.run.app",
    "https://ais-pre-pwmy5zemck42nwk7s5q7mq-49332687696.asia-east1.run.app",
    "https://ais-pre-og2hwn7bgqphr7cbx67aov-49332687696.asia-east1.run.app",
    "https://ais-pre-nibfwx7hiujwhnvxngfwf2-49332687696.asia-east1.run.app",
    "https://ais-pre-klggmabfw23vdwsy6s7jxs-49332687696.asia-east1.run.app",
    "https://ais-pre-x6qpsiogpaungpba2e7pu2-49332687696.asia-east1.run.app",
    "https://ais-pre-xdsf4csxxfhg5tlfc6qsil-49332687696.asia-east1.run.app",
    "https://ais-pre-jxgzbmqca4sgp4ntudicv7-49332687696.asia-east1.run.app",
    "https://ais-pre-venezxj3puxss4zbtwyfis-49332687696.asia-east1.run.app",
    "https://ais-pre-dh73kbzauyvja2mnssed3q-49332687696.asia-east1.run.app",
    "https://ais-pre-tjgjx6v3ej6cdiufclpnj2-49332687696.asia-east1.run.app",
    "https://ais-pre-npjgjawetbnhbxhrcxhpg2-49332687696.asia-east1.run.app",
    "https://ais-pre-pbu7p6mipvtfehnac5dx5u-49332687696.asia-east1.run.app",
]

# Terminals 61-90
urls_61_90 = [
    "https://ais-pre-nuezgc4afy6sme62bew44z-628481697275.asia-east1.run.app",
    "https://ais-pre-m6ehhbbroys3q7kw5rx2us-628481697275.asia-east1.run.app",
    "https://ais-pre-6txmhxwdigqnarocppeo6f-628481697275.asia-east1.run.app",
    "https://ais-pre-kxueivdzgg7xwhebvdgzuh-628481697275.asia-east1.run.app",
    "https://ais-pre-yg5c7gdhwoq6z6x7ijnets-628481697275.asia-east1.run.app",
    "https://ais-pre-zgx6y7v6fgja7l3z7cx3a7-628481697275.asia-east1.run.app",
    "https://ais-pre-p2jk5xrt23lv24afpxn6g2-628481697275.asia-east1.run.app",
    "https://ais-pre-hwck56pa5u43qof4pdkra5-628481697275.asia-east1.run.app",
    "https://ais-pre-arekyqa2ndg4lri3d4hl2m-628481697275.asia-east1.run.app",
    "https://ais-pre-spyxwjjhmovxmev7mbp6ns-628481697275.asia-east1.run.app",
    "https://ais-pre-ppokruzg3enc4ixrvtnart-628481697275.asia-east1.run.app",
    "https://ais-pre-mw6citgkmuyuhfy34hd6ee-628481697275.asia-east1.run.app",
    "https://ais-pre-ky3xn2zjdoagdoax6kaop3-628481697275.asia-east1.run.app",
    "https://ais-pre-ns7h4su4crebnwtzzywwbl-628481697275.asia-east1.run.app",
    "https://ais-pre-jlcv4m4m4hpsgt75wqdw6p-628481697275.asia-east1.run.app",
    "https://ais-pre-x67qcwvbmayicnjpezdvwf-628481697275.asia-east1.run.app",
    "https://ais-pre-tmyhorjrnvoigikyutnnod-628481697275.asia-east1.run.app",
    "https://ais-pre-yccxrvwl3qzmczyfcd3r57-628481697275.asia-east1.run.app",
    "https://ais-pre-3x2sf36fuavp7ua3nsjpre-628481697275.asia-east1.run.app",
    "https://ais-pre-yqeejrogmfdmkgfk4qndcp-628481697275.asia-east1.run.app",
    "https://ais-pre-in5oh4p4n7nhxw7fpocnpv-628481697275.asia-east1.run.app",
    "https://ais-pre-r2fozdrksbcvr4qhpubosy-628481697275.asia-east1.run.app",
    "https://ais-pre-qqp4sdgsb6xorv3gxtci3x-628481697275.asia-east1.run.app",
    "https://ais-pre-lkbzclwmyfueh4al4przju-628481697275.asia-east1.run.app",
    "https://ais-pre-2mnhcbkxycofgb6c5cppin-628481697275.asia-east1.run.app",
    "https://ais-pre-jpczx7cncsd6cbscogopw3-628481697275.asia-east1.run.app",
    "https://ais-pre-alh2dsvzhhul3rmgw7j4sv-628481697275.asia-east1.run.app",
    "https://ais-pre-7tqqdtn7xv5y74z54g6sfo-628481697275.asia-east1.run.app",
    "https://ais-pre-iulydxepty7epinwlovhis-628481697275.asia-east1.run.app",
    "https://ais-pre-uelstzyxoml33a672cjsjl-628481697275.asia-east1.run.app",
]

# Terminals 91-120
urls_91_120 = [
    "https://ais-pre-pkp2mar7g5siberzb4un3x-459098080991.asia-southeast1.run.app",
    "https://ais-pre-67bvdj3ktln2z2xikpn2fw-459098080991.asia-southeast1.run.app",
    "https://ais-pre-bsznentw3vksjh5wfhfzwk-459098080991.asia-southeast1.run.app",
    "https://ais-pre-3mr5absijns5hcgu7cwawf-459098080991.asia-southeast1.run.app",
    "https://ais-pre-bdc7t3mp4fbznsk3wv2k7n-459098080991.asia-southeast1.run.app",
    "https://ais-pre-nhc7jf6mjoewgcq4kyz4zi-459098080991.asia-southeast1.run.app",
    "https://ais-pre-tlebosklmkeknlvamnoee2-459098080991.asia-southeast1.run.app",
    "https://ais-pre-prbvr6md4yo6eglhjotpla-459098080991.asia-southeast1.run.app",
    "https://ais-pre-didh4hnob2f4vnkswoupbd-459098080991.asia-southeast1.run.app",
    "https://ais-pre-yzb7nw3f3hbrlvbmc47ujf-459098080991.asia-southeast1.run.app",
    "https://ais-pre-t7ysuvdsra3ub6tsxdght3-459098080991.asia-southeast1.run.app",
    "https://ais-pre-tcqpi4xnru777s5sezkxzf-459098080991.asia-southeast1.run.app",
    "https://ais-pre-jxuwxxqsdyhr37mvbsrmxz-459098080991.asia-southeast1.run.app",
    "https://ais-pre-qxepazeokjcfuaffje3avr-459098080991.asia-southeast1.run.app",
    "https://ais-pre-q5rsqjgl2erjgk4dzcf37h-459098080991.asia-southeast1.run.app",
    "https://ais-pre-wrs6cqk6i677q7eiaemzpq-459098080991.asia-southeast1.run.app",
    "https://ais-pre-oxqei3b2lkplswzeowupkm-459098080991.asia-southeast1.run.app",
    "https://ais-pre-qjurs4w7nvvhn5xi6gddmx-459098080991.asia-southeast1.run.app",
    "https://ais-pre-n2lqqp3yamu3qva35fffpc-459098080991.asia-southeast1.run.app",
    "https://ais-pre-es75dj56fznubovogjgr4w-459098080991.asia-southeast1.run.app",
    "https://ais-pre-ed3dgq5pibc6q3rojejbpb-459098080991.asia-southeast1.run.app",
    "https://ais-pre-4imguca5fpkwiucg4mvvh5-459098080991.asia-southeast1.run.app",
    "https://ais-pre-tinvp3hk3qccacunrorsmd-459098080991.asia-southeast1.run.app",
    "https://ais-pre-4ro7ouvhkq74i3la732bpa-459098080991.asia-southeast1.run.app",
    "https://ais-pre-6dqigvzmcqhdp6n3kofpmo-459098080991.asia-southeast1.run.app",
    "https://ais-pre-i4fmwrtu2z4ic3rmpkgb2f-459098080991.asia-southeast1.run.app",
    "https://ais-pre-njcml32rs2ck673epfjja2-459098080991.asia-southeast1.run.app",
    "https://ais-pre-nb45zsu7f4toepxodksehm-459098080991.asia-southeast1.run.app",
    "https://ais-pre-yqqry3zbzqdildicx4ymdg-459098080991.asia-southeast1.run.app",
    "https://ais-pre-fg3gvzmv4ca2fnfpjbviwt-459098080991.asia-southeast1.run.app",
]

# Terminals 121-150
urls_121_150 = [
    "https://ais-pre-2kkfeuhvcesukiphhd52ol-216967324577.asia-southeast1.run.app",
    "https://ais-pre-2lrry45a4oulyz665rw3uy-216967324577.asia-southeast1.run.app",
    "https://ais-pre-jg67felwa7wnwbfhjj2qcv-216967324577.asia-southeast1.run.app",
    "https://ais-pre-k4cylmwycio22rfxr2bxa5-216967324577.asia-southeast1.run.app",
    "https://ais-pre-ip6pfhx72sde7olxvu2tbt-216967324577.asia-southeast1.run.app",
    "https://ais-pre-k35373rickdrwyvjs7wk5z-216967324577.asia-southeast1.run.app",
    "https://ais-pre-hpeyssqty24gjwkpuzzop3-216967324577.asia-southeast1.run.app",
    "https://ais-pre-v4lqb3c2n4i6vnockt7yap-216967324577.asia-southeast1.run.app",
    "https://ais-pre-5p2hue6zpwawl2axhk6dac-216967324577.asia-southeast1.run.app",
    "https://ais-pre-ovsloxl34cn2sktyafs4b7-216967324577.asia-southeast1.run.app",
    "https://ais-pre-yep73o3ooa7v44u42jjjbh-216967324577.asia-southeast1.run.app",
    "https://ais-pre-uq4hl6ulns3k34q6g4ez4a-216967324577.asia-southeast1.run.app",
    "https://ais-pre-pygqszrsogjb53godkfhtt-216967324577.asia-southeast1.run.app",
    "https://ais-pre-ew5l5myrrdeo7clqfuv7xr-216967324577.asia-southeast1.run.app",
    "https://ais-pre-5yj7i74ygv564oj4wi6h4p-216967324577.asia-southeast1.run.app",
    "https://ais-pre-dz7rhx3hwxqbbwpbhii2k5-216967324577.asia-southeast1.run.app",
    "https://ais-pre-rjpzhrxmutwm6uathye7qj-216967324577.asia-southeast1.run.app",
    "https://ais-pre-3mrn4jdtm6lackxpegm6t3-216967324577.asia-southeast1.run.app",
    "https://ais-pre-rfdpwg7cfu3pdqumd7diz6-216967324577.asia-southeast1.run.app",
    "https://ais-pre-rqlvxsdgukkdrvudlrhupv-216967324577.asia-southeast1.run.app",
    "https://ais-pre-aeni6ot4xvnnlvgenm5e7k-216967324577.asia-southeast1.run.app",
    "https://ais-pre-osiziyjb2dayspq67vnrhh-216967324577.asia-southeast1.run.app",
    "https://ais-pre-6qbg4nhbokzzkuqn4to5ld-216967324577.asia-southeast1.run.app",
    "https://ais-pre-6vyjisce4us3x5oeh3wm3p-216967324577.asia-southeast1.run.app",
    "https://ais-pre-43namhcyuqcvdhv7bcnocl-216967324577.asia-southeast1.run.app",
    "https://ais-pre-sgxhsvfytlrv7mfwrrvrf7-216967324577.asia-southeast1.run.app",
    "https://ais-pre-irzay62zghl5q4353me4vh-216967324577.asia-southeast1.run.app",
    "https://ais-pre-ahkqsuihbejxpvee34xz3g-216967324577.asia-southeast1.run.app",
    "https://ais-pre-gbe7th3ws4lyqjjetwhvzi-216967324577.asia-southeast1.run.app",
    "https://ais-pre-yubvn257ednwpinon2yadx-216967324577.asia-southeast1.run.app",
]

# Build TERMINALS list
for i, url in enumerate(urls_1_30, start=1):
    TERMINALS.append([i, f"Terminal {i}", url.split('-')[2].split('.')[0] if 'ais-pre' in url else f"miner{i}", url])

for i, url in enumerate(urls_31_60, start=31):
    TERMINALS.append([i, f"Terminal {i}", url.split('-')[2].split('.')[0] if 'ais-pre' in url else f"miner{i}", url])

for i, url in enumerate(urls_61_90, start=61):
    TERMINALS.append([i, f"Terminal {i}", url.split('-')[2].split('.')[0] if 'ais-pre' in url else f"miner{i}", url])

for i, url in enumerate(urls_91_120, start=91):
    TERMINALS.append([i, f"Terminal {i}", url.split('-')[2].split('.')[0] if 'ais-pre' in url else f"miner{i}", url])

for i, url in enumerate(urls_121_150, start=121):
    TERMINALS.append([i, f"Terminal {i}", url.split('-')[2].split('.')[0] if 'ais-pre' in url else f"miner{i}", url])

# ==================== FUNCTIONS ====================
def log(msg): print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
def send_tg(title, msg, emoji="📘"): telegram.send_message(f"{emoji} <b>{title}</b>\n{msg}")

def get_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB ({ram.percent}%)"
    except:
        return "N/A"

def take_screenshot(filename="screenshot.png"):
    """Take screenshot - only works if display is available"""
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return filename
    except Exception as e:
        log(f"Screenshot error (may be headless): {e}")
        return None

def get_uuid():
    try:
        r = requests.get(f"{API_BASE}/address/{WALLET_ADDRESS}?coin={COIN}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code == 200:
            return r.json().get('data', {}).get('uuid')
        return None
    except Exception as e:
        log(f"Error getting UUID: {e}")
        return None

def check_status(miner_name, uuid):
    try:
        r = requests.get(f"{API_BASE}/account/{uuid}/workers", headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code == 200:
            workers = r.json().get('data', {}).get('randomx', {}).get('workers', [])
            for w in workers:
                if w.get('name') == miner_name:
                    return w.get('online', False)
        return False
    except:
        return False

def open_window(browser_path: str, browser_type: str, url: str, name: str):
    try:
        cmd = get_browser_command(browser_path, browser_type, url)
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        log(f"Failed to open {name}: {e}")
        return False

def close_window_by_pid(process):
    try:
        if process:
            process.terminate()
            process.wait(timeout=5)
            return True
    except:
        pass
    return False

def close_window_by_name(miner_name: str):
    """Close browser window containing specific miner name"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] in ['firefox', 'firefox-bin', 'chrome', 'chromium', 'chromium-browser']:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if miner_name in cmdline:
                        proc.terminate()
                        proc.wait(timeout=5)
                        return True
            except:
                pass
        return False
    except:
        return False

def run_workflow(browser_path: str, browser_type: str):
    total = len(TERMINALS)
    batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    log(f"Ubuntu RDP Miner Started")
    log(f"Browser: {browser_type} at {browser_path}")
    log(f"Total Terminals: {total}, Batch size: {BATCH_SIZE}, Batches: {batches}")
    log(f"Check interval: {CHECK_INTERVAL//60} minutes")
    log(f"System: {get_system_info()}")
    
    send_tg("WORKFLOW STARTED (Ubuntu)", f"Total: {total}\nBrowser: {browser_type}\n{get_system_info()}", "🚀")
    
    uuid = get_uuid()
    if not uuid:
        send_tg("ERROR", "Failed to get UUID from Unmineable API", "❌")
        return
    
    log(f"UUID: {uuid[:8]}...")
    send_tg("API CONNECTED", f"UUID: {uuid[:8]}...", "✅")
    
    # ========== OPEN FIRST BATCH (for screenshot) ==========
    log("\nOpening BATCH 1 for screenshot proof...")
    first_batch = TERMINALS[0:BATCH_SIZE]
    for m in first_batch:
        open_window(browser_path, browser_type, m[3], m[1])
        log(f"   Opened {m[1]}")
        time.sleep(2)
    
    log("Batch 1 opened successfully")
    send_tg("BATCH 1 OPENED", f"Opened {len(first_batch)} terminals", "✅")
    
    # Try to take screenshot (may fail in headless)
    time.sleep(30)
    ss = take_screenshot(f"screenshot_batch1.png")
    if ss:
        caption = f"📸 BATCH 1 SCREENSHOT\nTerminals 1-{BATCH_SIZE}\n{get_system_info()}"
        telegram.send_photo(ss, caption)
        log("Screenshot sent to Telegram")
    else:
        log("Screenshot not available (headless mode)")
    
    time.sleep(GAP_BETWEEN_BATCHES)
    
    # ========== OPEN REMAINING BATCHES ==========
    for b in range(1, batches):
        start = b * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = TERMINALS[start:end]
        
        log(f"Batch {b+1}/{batches}")
        for m in batch:
            open_window(browser_path, browser_type, m[3], m[1])
            log(f"   Opened {m[1]}")
            time.sleep(2)
        
        if end < total:
            log(f"Waiting {GAP_BETWEEN_BATCHES} seconds...")
            time.sleep(GAP_BETWEEN_BATCHES)
    
    log(f"\nAll {total} terminals opened!")
    send_tg("ALL OPENED", f"All {total} terminals opened successfully!\n{get_system_info()}", "✅")
    
    # ========== MONITORING LOOP ==========
    log(f"\nStarting monitoring (every {CHECK_INTERVAL//60} minutes)")
    send_tg("MONITORING STARTED", f"Checking every {CHECK_INTERVAL//60} minutes via API", "🔍")
    
    while True:
        time.sleep(CHECK_INTERVAL)
        
        log(f"\nChecking status...")
        offline = []
        online = 0
        
        for m in TERMINALS:
            if check_status(m[2], uuid):
                online += 1
                log(f"   ONLINE: {m[1]}")
            else:
                log(f"   OFFLINE: {m[1]}")
                offline.append(m)
        
        success_rate = (online * 100) / total if total > 0 else 0
        
        if offline:
            send_tg(f"STATUS - {len(offline)} OFFLINE", f"Ubuntu: {online}/{total} ONLINE ({success_rate:.1f}%)\n{get_system_info()}", "⚠️")
            
            log(f"Restarting {len(offline)} offline miners...")
            send_tg("RESTARTING", f"Restarting {len(offline)} offline miners...", "🔄")
            
            for m in offline:
                log(f"   Restarting {m[1]}...")
                close_window_by_name(m[2])
                time.sleep(2)
                open_window(browser_path, browser_type, m[3], m[1])
                time.sleep(3)
            
            send_tg("RESTART COMPLETE", f"Restarted {len(offline)} miners", "✅")
        else:
            send_tg("STATUS - ALL ONLINE", f"Ubuntu: {online}/{total} ONLINE (100%)\n{get_system_info()}", "✅")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("UBUNTU RDP MINER AUTOMATION - Terminals 1-150")
    print("="*60 + "\n")
    
    # Check and setup browser
    browser_path, browser_type = check_browser()
    if not browser_path:
        print("[ERROR] No browser found and installation failed!")
        send_tg("ERROR", "No browser found and installation failed!", "❌")
        sys.exit(1)
    
    print(f"[OK] Using {browser_type}: {browser_path}")
    
    # Check if display is available for screenshots
    if os.environ.get('DISPLAY'):
        print(f"[OK] Display available: {os.environ.get('DISPLAY')}")
    else:
        print("[WARN] No DISPLAY set. Screenshots will not work.")
    
    # Run workflow
    run_workflow(browser_path, browser_type)
