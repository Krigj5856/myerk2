#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miner Automation - Railway Ubuntu Desktop
3 Windows/Batch | 1 Min Active | Batch Waits for Close | 6 Min Check | All 270 Terminals
"""

import os
import sys
import subprocess
import time
import signal
import threading
from datetime import datetime
from typing import Optional, List

# ==================== INSTALL DEPENDENCIES ====================
def ensure_dependencies():
    try:
        import requests
        import psutil
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "psutil", "--quiet"])

ensure_dependencies()

import requests
import psutil

# ==================== TELEGRAM ====================
TELEGRAM_BOT_TOKEN = "8624711171:AAEqWiSMbrxWl1N3Hw22IZgqENicqJXq03g"
TELEGRAM_CHAT_ID = "6955911349"

class TelegramLogger:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    def send_message(self, message: str):
        try:
            requests.post(f"{self.base_url}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
        except:
            pass
    def send_log(self, message: str, level: str = "INFO"):
        emojis = {"INFO": "📘", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", 
                  "ONLINE": "🟢", "OFFLINE": "🔴", "RESTART": "🔄", "START": "🚀", 
                  "CHECK": "🔍", "CLOSE": "🚪", "OPEN": "📂"}
        emoji = emojis.get(level, "📝")
        self.send_message(f"{emoji} <b>{level}</b>\n{message}")

telegram = TelegramLogger()

# ==================== CONFIG ====================
FIREFOX_CMD = "firefox"
API_BASE = "https://api.unmineable.com/v5"
WALLET_ADDRESS = "nano_1g97x3h6wxd4h577p6dricapigs78ccc7tcowjfm67hewsmg7qob4xwc8jak"
COIN = "NANO"

BATCH_SIZE = 3
WINDOW_ACTIVE_TIME = 60  # 1 minute
CHECK_INTERVAL = 360  # 6 minutes

# ==================== ALL 270 TERMINALS ====================
ALL_TERMINALS = [
    # Terminals 1-30
    [1, "Terminal 1", "lpa5neewvrg3efhfoqiuc5", "https://ais-pre-lpa5neewvrg3efhfoqiuc5-158414749269.asia-east1.run.app"],
    [2, "Terminal 2", "u27dqik55hsbpuc3a4zdjg", "https://ais-pre-u27dqik55hsbpuc3a4zdjg-158414749269.asia-east1.run.app"],
    [3, "Terminal 3", "s46wg4fbogdnawfz7lponw", "https://ais-pre-s46wg4fbogdnawfz7lponw-158414749269.asia-east1.run.app"],
    [4, "Terminal 4", "xnlziqjgwx25kek5dt7vjg", "https://ais-pre-xnlziqjgwx25kek5dt7vjg-158414749269.asia-east1.run.app"],
    [5, "Terminal 5", "fnzsax2ntgpumss2fv7gbs", "https://ais-pre-fnzsax2ntgpumss2fv7gbs-158414749269.asia-east1.run.app"],
    [6, "Terminal 6", "asmthlh2hwe2zc5aucqkux", "https://ais-pre-asmthlh2hwe2zc5aucqkux-158414749269.asia-east1.run.app"],
    [7, "Terminal 7", "plttdjcx2xfi7ae5fyu6mx", "https://ais-pre-plttdjcx2xfi7ae5fyu6mx-158414749269.asia-east1.run.app"],
    [8, "Terminal 8", "l4brlflom366xidrwprvjb", "https://ais-pre-l4brlflom366xidrwprvjb-158414749269.asia-east1.run.app"],
    [9, "Terminal 9", "kgpcawracefzloi6423wwz", "https://ais-pre-kgpcawracefzloi6423wwz-158414749269.asia-east1.run.app"],
    [10, "Terminal 10", "yeb5zgkfkptb4g2n7sw35p", "https://ais-pre-yeb5zgkfkptb4g2n7sw35p-158414749269.asia-east1.run.app"],
    [11, "Terminal 11", "s4akyhx55nwwsd7eix526w", "https://ais-pre-s4akyhx55nwwsd7eix526w-158414749269.asia-east1.run.app"],
    [12, "Terminal 12", "acjdhdwko7xatspy2gsc6j", "https://ais-pre-acjdhdwko7xatspy2gsc6j-158414749269.asia-east1.run.app"],
    [13, "Terminal 13", "sgqlk63rywltds2oqvgfrk", "https://ais-pre-sgqlk63rywltds2oqvgfrk-158414749269.asia-east1.run.app"],
    [14, "Terminal 14", "lcfu33gv6j7wq3jvzsmiyk", "https://ais-pre-lcfu33gv6j7wq3jvzsmiyk-158414749269.asia-east1.run.app"],
    [15, "Terminal 15", "3fggqei6e4uumtzy6pkao6", "https://ais-pre-3fggqei6e4uumtzy6pkao6-158414749269.asia-east1.run.app"],
    [16, "Terminal 16", "e5rt6ghxcshonxkr3n2po3", "https://ais-pre-e5rt6ghxcshonxkr3n2po3-158414749269.asia-east1.run.app"],
    [17, "Terminal 17", "ag7j6atapmrwbqd24hkmp6", "https://ais-pre-ag7j6atapmrwbqd24hkmp6-158414749269.asia-east1.run.app"],
    [18, "Terminal 18", "oyoftfifg6xqgv4ehkhbpt", "https://ais-pre-oyoftfifg6xqgv4ehkhbpt-158414749269.asia-east1.run.app"],
    [19, "Terminal 19", "yuemoooayebljtmf7jlhus", "https://ais-pre-yuemoooayebljtmf7jlhus-158414749269.asia-east1.run.app"],
    [20, "Terminal 20", "af6dupaeexazcqo4rjfoho", "https://ais-pre-af6dupaeexazcqo4rjfoho-158414749269.asia-east1.run.app"],
    [21, "Terminal 21", "kg2efziimzs64e3573gx2s", "https://ais-pre-kg2efziimzs64e3573gx2s-158414749269.asia-east1.run.app"],
    [22, "Terminal 22", "hfsvrh2trwclm5qvxyfxsf", "https://ais-pre-hfsvrh2trwclm5qvxyfxsf-158414749269.asia-east1.run.app"],
    [23, "Terminal 23", "fikatfynsoebnu65bjwjyv", "https://ais-pre-fikatfynsoebnu65bjwjyv-158414749269.asia-east1.run.app"],
    [24, "Terminal 24", "7g6ghr4tgbx4wnzvvl5to2", "https://ais-pre-7g6ghr4tgbx4wnzvvl5to2-158414749269.asia-east1.run.app"],
    [25, "Terminal 25", "434666jxs4tm7ei52tgsr4", "https://ais-pre-434666jxs4tm7ei52tgsr4-158414749269.asia-east1.run.app"],
    [26, "Terminal 26", "wwaaefvpl6lmvrqk3lh6u7", "https://ais-pre-wwaaefvpl6lmvrqk3lh6u7-158414749269.asia-east1.run.app"],
    [27, "Terminal 27", "22twhibrd5ag2smw4t6iuw", "https://ais-pre-22twhibrd5ag2smw4t6iuw-158414749269.asia-east1.run.app"],
    [28, "Terminal 28", "wx3rtfealli6p4qcqtxjdd", "https://ais-pre-wx3rtfealli6p4qcqtxjdd-158414749269.asia-east1.run.app"],
    [29, "Terminal 29", "4elhve7u4jvldqq3qhdduo", "https://ais-pre-4elhve7u4jvldqq3qhdduo-158414749269.asia-east1.run.app"],
    [30, "Terminal 30", "wfwhkeqvy23mf2h5kheouz", "https://ais-pre-wfwhkeqvy23mf2h5kheouz-158414749269.asia-east1.run.app"],
    
    # Terminals 31-60
    [31, "Terminal 31", "l4nexpjplufhhrp3rg2mnr", "https://ais-pre-l4nexpjplufhhrp3rg2mnr-49332687696.asia-east1.run.app"],
    [32, "Terminal 32", "xrgbkmdurfjazearttecfg", "https://ais-pre-xrgbkmdurfjazearttecfg-49332687696.asia-east1.run.app"],
    [33, "Terminal 33", "r7cl5ikxlphlx2jnqfr4n3", "https://ais-pre-r7cl5ikxlphlx2jnqfr4n3-49332687696.asia-east1.run.app"],
    [34, "Terminal 34", "lmkapxey2y4blw6wv2dt5i", "https://ais-pre-lmkapxey2y4blw6wv2dt5i-49332687696.asia-east1.run.app"],
    [35, "Terminal 35", "ctceihay3r4nctd5gsps7y", "https://ais-pre-ctceihay3r4nctd5gsps7y-49332687696.asia-east1.run.app"],
    [36, "Terminal 36", "thtwvzhh6yapos3lglf5z3", "https://ais-pre-thtwvzhh6yapos3lglf5z3-49332687696.asia-east1.run.app"],
    [37, "Terminal 37", "pupk4rdctuhhkoxcb4ogoj", "https://ais-pre-pupk4rdctuhhkoxcb4ogoj-49332687696.asia-east1.run.app"],
    [38, "Terminal 38", "j53c3ev3l7r2bxzxt23kta", "https://ais-pre-j53c3ev3l7r2bxzxt23kta-49332687696.asia-east1.run.app"],
    [39, "Terminal 39", "ozd2yr57dcdy66vn25p6sa", "https://ais-pre-ozd2yr57dcdy66vn25p6sa-49332687696.asia-east1.run.app"],
    [40, "Terminal 40", "6cgwknlc2logtvfnkp5kv4", "https://ais-pre-6cgwknlc2logtvfnkp5kv4-49332687696.asia-east1.run.app"],
    [41, "Terminal 41", "pk4iomeemgbzyjdnrmzbls", "https://ais-pre-pk4iomeemgbzyjdnrmzbls-49332687696.asia-east1.run.app"],
    [42, "Terminal 42", "bi7j3jwv6bys5sukvgnrzs", "https://ais-pre-bi7j3jwv6bys5sukvgnrzs-49332687696.asia-east1.run.app"],
    [43, "Terminal 43", "waqj65qludc3ao6mzxkv67", "https://ais-pre-waqj65qludc3ao6mzxkv67-49332687696.asia-east1.run.app"],
    [44, "Terminal 44", "7a6bv6o77z65omxcamt3km", "https://ais-pre-7a6bv6o77z65omxcamt3km-49332687696.asia-east1.run.app"],
    [45, "Terminal 45", "65645qtry5k6oj4quvle37", "https://ais-pre-65645qtry5k6oj4quvle37-49332687696.asia-east1.run.app"],
    [46, "Terminal 46", "lkvnsbtsrygnajjz3lwbe3", "https://ais-pre-lkvnsbtsrygnajjz3lwbe3-49332687696.asia-east1.run.app"],
    [47, "Terminal 47", "npvl6zxgbscqc37qgqw27c", "https://ais-pre-npvl6zxgbscqc37qgqw27c-49332687696.asia-east1.run.app"],
    [48, "Terminal 48", "fop7mm76x54b5v2pffflv6", "https://ais-pre-fop7mm76x54b5v2pffflv6-49332687696.asia-east1.run.app"],
    [49, "Terminal 49", "pwmy5zemck42nwk7s5q7mq", "https://ais-pre-pwmy5zemck42nwk7s5q7mq-49332687696.asia-east1.run.app"],
    [50, "Terminal 50", "og2hwn7bgqphr7cbx67aov", "https://ais-pre-og2hwn7bgqphr7cbx67aov-49332687696.asia-east1.run.app"],
    [51, "Terminal 51", "nibfwx7hiujwhnvxngfwf2", "https://ais-pre-nibfwx7hiujwhnvxngfwf2-49332687696.asia-east1.run.app"],
    [52, "Terminal 52", "klggmabfw23vdwsy6s7jxs", "https://ais-pre-klggmabfw23vdwsy6s7jxs-49332687696.asia-east1.run.app"],
    [53, "Terminal 53", "x6qpsiogpaungpba2e7pu2", "https://ais-pre-x6qpsiogpaungpba2e7pu2-49332687696.asia-east1.run.app"],
    [54, "Terminal 54", "xdsf4csxxfhg5tlfc6qsil", "https://ais-pre-xdsf4csxxfhg5tlfc6qsil-49332687696.asia-east1.run.app"],
    [55, "Terminal 55", "jxgzbmqca4sgp4ntudicv7", "https://ais-pre-jxgzbmqca4sgp4ntudicv7-49332687696.asia-east1.run.app"],
    [56, "Terminal 56", "venezxj3puxss4zbtwyfis", "https://ais-pre-venezxj3puxss4zbtwyfis-49332687696.asia-east1.run.app"],
    [57, "Terminal 57", "dh73kbzauyvja2mnssed3q", "https://ais-pre-dh73kbzauyvja2mnssed3q-49332687696.asia-east1.run.app"],
    [58, "Terminal 58", "tjgjx6v3ej6cdiufclpnj2", "https://ais-pre-tjgjx6v3ej6cdiufclpnj2-49332687696.asia-east1.run.app"],
    [59, "Terminal 59", "npjgjawetbnhbxhrcxhpg2", "https://ais-pre-npjgjawetbnhbxhrcxhpg2-49332687696.asia-east1.run.app"],
    [60, "Terminal 60", "pbu7p6mipvtfehnac5dx5u", "https://ais-pre-pbu7p6mipvtfehnac5dx5u-49332687696.asia-east1.run.app"],

    # Terminals 61-90
    [61, "Terminal 61", "nuezgc4afy6sme62bew44z", "https://ais-pre-nuezgc4afy6sme62bew44z-628481697275.asia-east1.run.app"],
    [62, "Terminal 62", "m6ehhbbroys3q7kw5rx2us", "https://ais-pre-m6ehhbbroys3q7kw5rx2us-628481697275.asia-east1.run.app"],
    [63, "Terminal 63", "6txmhxwdigqnarocppeo6f", "https://ais-pre-6txmhxwdigqnarocppeo6f-628481697275.asia-east1.run.app"],
    [64, "Terminal 64", "kxueivdzgg7xwhebvdgzuh", "https://ais-pre-kxueivdzgg7xwhebvdgzuh-628481697275.asia-east1.run.app"],
    [65, "Terminal 65", "yg5c7gdhwoq6z6x7ijnets", "https://ais-pre-yg5c7gdhwoq6z6x7ijnets-628481697275.asia-east1.run.app"],
    [66, "Terminal 66", "zgx6y7v6fgja7l3z7cx3a7", "https://ais-pre-zgx6y7v6fgja7l3z7cx3a7-628481697275.asia-east1.run.app"],
    [67, "Terminal 67", "p2jk5xrt23lv24afpxn6g2", "https://ais-pre-p2jk5xrt23lv24afpxn6g2-628481697275.asia-east1.run.app"],
    [68, "Terminal 68", "hwck56pa5u43qof4pdkra5", "https://ais-pre-hwck56pa5u43qof4pdkra5-628481697275.asia-east1.run.app"],
    [69, "Terminal 69", "arekyqa2ndg4lri3d4hl2m", "https://ais-pre-arekyqa2ndg4lri3d4hl2m-628481697275.asia-east1.run.app"],
    [70, "Terminal 70", "spyxwjjhmovxmev7mbp6ns", "https://ais-pre-spyxwjjhmovxmev7mbp6ns-628481697275.asia-east1.run.app"],
    [71, "Terminal 71", "ppokruzg3enc4ixrvtnart", "https://ais-pre-ppokruzg3enc4ixrvtnart-628481697275.asia-east1.run.app"],
    [72, "Terminal 72", "mw6citgkmuyuhfy34hd6ee", "https://ais-pre-mw6citgkmuyuhfy34hd6ee-628481697275.asia-east1.run.app"],
    [73, "Terminal 73", "ky3xn2zjdoagdoax6kaop3", "https://ais-pre-ky3xn2zjdoagdoax6kaop3-628481697275.asia-east1.run.app"],
    [74, "Terminal 74", "ns7h4su4crebnwtzzywwbl", "https://ais-pre-ns7h4su4crebnwtzzywwbl-628481697275.asia-east1.run.app"],
    [75, "Terminal 75", "jlcv4m4m4hpsgt75wqdw6p", "https://ais-pre-jlcv4m4m4hpsgt75wqdw6p-628481697275.asia-east1.run.app"],
    [76, "Terminal 76", "x67qcwvbmayicnjpezdvwf", "https://ais-pre-x67qcwvbmayicnjpezdvwf-628481697275.asia-east1.run.app"],
    [77, "Terminal 77", "tmyhorjrnvoigikyutnnod", "https://ais-pre-tmyhorjrnvoigikyutnnod-628481697275.asia-east1.run.app"],
    [78, "Terminal 78", "yccxrvwl3qzmczyfcd3r57", "https://ais-pre-yccxrvwl3qzmczyfcd3r57-628481697275.asia-east1.run.app"],
    [79, "Terminal 79", "3x2sf36fuavp7ua3nsjpre", "https://ais-pre-3x2sf36fuavp7ua3nsjpre-628481697275.asia-east1.run.app"],
    [80, "Terminal 80", "yqeejrogmfdmkgfk4qndcp", "https://ais-pre-yqeejrogmfdmkgfk4qndcp-628481697275.asia-east1.run.app"],
    [81, "Terminal 81", "in5oh4p4n7nhxw7fpocnpv", "https://ais-pre-in5oh4p4n7nhxw7fpocnpv-628481697275.asia-east1.run.app"],
    [82, "Terminal 82", "r2fozdrksbcvr4qhpubosy", "https://ais-pre-r2fozdrksbcvr4qhpubosy-628481697275.asia-east1.run.app"],
    [83, "Terminal 83", "qqp4sdgsb6xorv3gxtci3x", "https://ais-pre-qqp4sdgsb6xorv3gxtci3x-628481697275.asia-east1.run.app"],
    [84, "Terminal 84", "lkbzclwmyfueh4al4przju", "https://ais-pre-lkbzclwmyfueh4al4przju-628481697275.asia-east1.run.app"],
    [85, "Terminal 85", "2mnhcbkxycofgb6c5cppin", "https://ais-pre-2mnhcbkxycofgb6c5cppin-628481697275.asia-east1.run.app"],
    [86, "Terminal 86", "jpczx7cncsd6cbscogopw3", "https://ais-pre-jpczx7cncsd6cbscogopw3-628481697275.asia-east1.run.app"],
    [87, "Terminal 87", "alh2dsvzhhul3rmgw7j4sv", "https://ais-pre-alh2dsvzhhul3rmgw7j4sv-628481697275.asia-east1.run.app"],
    [88, "Terminal 88", "7tqqdtn7xv5y74z54g6sfo", "https://ais-pre-7tqqdtn7xv5y74z54g6sfo-628481697275.asia-east1.run.app"],
    [89, "Terminal 89", "iulydxepty7epinwlovhis", "https://ais-pre-iulydxepty7epinwlovhis-628481697275.asia-east1.run.app"],
    [90, "Terminal 90", "uelstzyxoml33a672cjsjl", "https://ais-pre-uelstzyxoml33a672cjsjl-628481697275.asia-east1.run.app"],

    # Terminals 91-120
    [91, "Terminal 91", "pkp2mar7g5siberzb4un3x", "https://ais-pre-pkp2mar7g5siberzb4un3x-459098080991.asia-southeast1.run.app"],
    [92, "Terminal 92", "67bvdj3ktln2z2xikpn2fw", "https://ais-pre-67bvdj3ktln2z2xikpn2fw-459098080991.asia-southeast1.run.app"],
    [93, "Terminal 93", "bsznentw3vksjh5wfhfzwk", "https://ais-pre-bsznentw3vksjh5wfhfzwk-459098080991.asia-southeast1.run.app"],
    [94, "Terminal 94", "3mr5absijns5hcgu7cwawf", "https://ais-pre-3mr5absijns5hcgu7cwawf-459098080991.asia-southeast1.run.app"],
    [95, "Terminal 95", "bdc7t3mp4fbznsk3wv2k7n", "https://ais-pre-bdc7t3mp4fbznsk3wv2k7n-459098080991.asia-southeast1.run.app"],
    [96, "Terminal 96", "nhc7jf6mjoewgcq4kyz4zi", "https://ais-pre-nhc7jf6mjoewgcq4kyz4zi-459098080991.asia-southeast1.run.app"],
    [97, "Terminal 97", "tlebosklmkeknlvamnoee2", "https://ais-pre-tlebosklmkeknlvamnoee2-459098080991.asia-southeast1.run.app"],
    [98, "Terminal 98", "prbvr6md4yo6eglhjotpla", "https://ais-pre-prbvr6md4yo6eglhjotpla-459098080991.asia-southeast1.run.app"],
    [99, "Terminal 99", "didh4hnob2f4vnkswoupbd", "https://ais-pre-didh4hnob2f4vnkswoupbd-459098080991.asia-southeast1.run.app"],
    [100, "Terminal 100", "yzb7nw3f3hbrlvbmc47ujf", "https://ais-pre-yzb7nw3f3hbrlvbmc47ujf-459098080991.asia-southeast1.run.app"],
    [101, "Terminal 101", "t7ysuvdsra3ub6tsxdght3", "https://ais-pre-t7ysuvdsra3ub6tsxdght3-459098080991.asia-southeast1.run.app"],
    [102, "Terminal 102", "tcqpi4xnru777s5sezkxzf", "https://ais-pre-tcqpi4xnru777s5sezkxzf-459098080991.asia-southeast1.run.app"],
    [103, "Terminal 103", "jxuwxxqsdyhr37mvbsrmxz", "https://ais-pre-jxuwxxqsdyhr37mvbsrmxz-459098080991.asia-southeast1.run.app"],
    [104, "Terminal 104", "qxepazeokjcfuaffje3avr", "https://ais-pre-qxepazeokjcfuaffje3avr-459098080991.asia-southeast1.run.app"],
    [105, "Terminal 105", "q5rsqjgl2erjgk4dzcf37h", "https://ais-pre-q5rsqjgl2erjgk4dzcf37h-459098080991.asia-southeast1.run.app"],
    [106, "Terminal 106", "wrs6cqk6i677q7eiaemzpq", "https://ais-pre-wrs6cqk6i677q7eiaemzpq-459098080991.asia-southeast1.run.app"],
    [107, "Terminal 107", "oxqei3b2lkplswzeowupkm", "https://ais-pre-oxqei3b2lkplswzeowupkm-459098080991.asia-southeast1.run.app"],
    [108, "Terminal 108", "qjurs4w7nvvhn5xi6gddmx", "https://ais-pre-qjurs4w7nvvhn5xi6gddmx-459098080991.asia-southeast1.run.app"],
    [109, "Terminal 109", "n2lqqp3yamu3qva35fffpc", "https://ais-pre-n2lqqp3yamu3qva35fffpc-459098080991.asia-southeast1.run.app"],
    [110, "Terminal 110", "es75dj56fznubovogjgr4w", "https://ais-pre-es75dj56fznubovogjgr4w-459098080991.asia-southeast1.run.app"],
    [111, "Terminal 111", "ed3dgq5pibc6q3rojejbpb", "https://ais-pre-ed3dgq5pibc6q3rojejbpb-459098080991.asia-southeast1.run.app"],
    [112, "Terminal 112", "4imguca5fpkwiucg4mvvh5", "https://ais-pre-4imguca5fpkwiucg4mvvh5-459098080991.asia-southeast1.run.app"],
    [113, "Terminal 113", "tinvp3hk3qccacunrorsmd", "https://ais-pre-tinvp3hk3qccacunrorsmd-459098080991.asia-southeast1.run.app"],
    [114, "Terminal 114", "4ro7ouvhkq74i3la732bpa", "https://ais-pre-4ro7ouvhkq74i3la732bpa-459098080991.asia-southeast1.run.app"],
    [115, "Terminal 115", "6dqigvzmcqhdp6n3kofpmo", "https://ais-pre-6dqigvzmcqhdp6n3kofpmo-459098080991.asia-southeast1.run.app"],
    [116, "Terminal 116", "i4fmwrtu2z4ic3rmpkgb2f", "https://ais-pre-i4fmwrtu2z4ic3rmpkgb2f-459098080991.asia-southeast1.run.app"],
    [117, "Terminal 117", "njcml32rs2ck673epfjja2", "https://ais-pre-njcml32rs2ck673epfjja2-459098080991.asia-southeast1.run.app"],
    [118, "Terminal 118", "nb45zsu7f4toepxodksehm", "https://ais-pre-nb45zsu7f4toepxodksehm-459098080991.asia-southeast1.run.app"],
    [119, "Terminal 119", "yqqry3zbzqdildicx4ymdg", "https://ais-pre-yqqry3zbzqdildicx4ymdg-459098080991.asia-southeast1.run.app"],
    [120, "Terminal 120", "fg3gvzmv4ca2fnfpjbviwt", "https://ais-pre-fg3gvzmv4ca2fnfpjbviwt-459098080991.asia-southeast1.run.app"],

    # Terminals 121-150
    [121, "Terminal 121", "2kkfeuhvcesukiphhd52ol", "https://ais-pre-2kkfeuhvcesukiphhd52ol-216967324577.asia-southeast1.run.app"],
    [122, "Terminal 122", "2lrry45a4oulyz665rw3uy", "https://ais-pre-2lrry45a4oulyz665rw3uy-216967324577.asia-southeast1.run.app"],
    [123, "Terminal 123", "jg67felwa7wnwbfhjj2qcv", "https://ais-pre-jg67felwa7wnwbfhjj2qcv-216967324577.asia-southeast1.run.app"],
    [124, "Terminal 124", "k4cylmwycio22rfxr2bxa5", "https://ais-pre-k4cylmwycio22rfxr2bxa5-216967324577.asia-southeast1.run.app"],
    [125, "Terminal 125", "ip6pfhx72sde7olxvu2tbt", "https://ais-pre-ip6pfhx72sde7olxvu2tbt-216967324577.asia-southeast1.run.app"],
    [126, "Terminal 126", "k35373rickdrwyvjs7wk5z", "https://ais-pre-k35373rickdrwyvjs7wk5z-216967324577.asia-southeast1.run.app"],
    [127, "Terminal 127", "hpeyssqty24gjwkpuzzop3", "https://ais-pre-hpeyssqty24gjwkpuzzop3-216967324577.asia-southeast1.run.app"],
    [128, "Terminal 128", "v4lqb3c2n4i6vnockt7yap", "https://ais-pre-v4lqb3c2n4i6vnockt7yap-216967324577.asia-southeast1.run.app"],
    [129, "Terminal 129", "5p2hue6zpwawl2axhk6dac", "https://ais-pre-5p2hue6zpwawl2axhk6dac-216967324577.asia-southeast1.run.app"],
    [130, "Terminal 130", "ovsloxl34cn2sktyafs4b7", "https://ais-pre-ovsloxl34cn2sktyafs4b7-216967324577.asia-southeast1.run.app"],
    [131, "Terminal 131", "yep73o3ooa7v44u42jjjbh", "https://ais-pre-yep73o3ooa7v44u42jjjbh-216967324577.asia-southeast1.run.app"],
    [132, "Terminal 132", "uq4hl6ulns3k34q6g4ez4a", "https://ais-pre-uq4hl6ulns3k34q6g4ez4a-216967324577.asia-southeast1.run.app"],
    [133, "Terminal 133", "pygqszrsogjb53godkfhtt", "https://ais-pre-pygqszrsogjb53godkfhtt-216967324577.asia-southeast1.run.app"],
    [134, "Terminal 134", "ew5l5myrrdeo7clqfuv7xr", "https://ais-pre-ew5l5myrrdeo7clqfuv7xr-216967324577.asia-southeast1.run.app"],
    [135, "Terminal 135", "5yj7i74ygv564oj4wi6h4p", "https://ais-pre-5yj7i74ygv564oj4wi6h4p-216967324577.asia-southeast1.run.app"],
    [136, "Terminal 136", "dz7rhx3hwxqbbwpbhii2k5", "https://ais-pre-dz7rhx3hwxqbbwpbhii2k5-216967324577.asia-southeast1.run.app"],
    [137, "Terminal 137", "rjpzhrxmutwm6uathye7qj", "https://ais-pre-rjpzhrxmutwm6uathye7qj-216967324577.asia-southeast1.run.app"],
    [138, "Terminal 138", "3mrn4jdtm6lackxpegm6t3", "https://ais-pre-3mrn4jdtm6lackxpegm6t3-216967324577.asia-southeast1.run.app"],
    [139, "Terminal 139", "rfdpwg7cfu3pdqumd7diz6", "https://ais-pre-rfdpwg7cfu3pdqumd7diz6-216967324577.asia-southeast1.run.app"],
    [140, "Terminal 140", "rqlvxsdgukkdrvudlrhupv", "https://ais-pre-rqlvxsdgukkdrvudlrhupv-216967324577.asia-southeast1.run.app"],
    [141, "Terminal 141", "aeni6ot4xvnnlvgenm5e7k", "https://ais-pre-aeni6ot4xvnnlvgenm5e7k-216967324577.asia-southeast1.run.app"],
    [142, "Terminal 142", "osiziyjb2dayspq67vnrhh", "https://ais-pre-osiziyjb2dayspq67vnrhh-216967324577.asia-southeast1.run.app"],
    [143, "Terminal 143", "6qbg4nhbokzzkuqn4to5ld", "https://ais-pre-6qbg4nhbokzzkuqn4to5ld-216967324577.asia-southeast1.run.app"],
    [144, "Terminal 144", "6vyjisce4us3x5oeh3wm3p", "https://ais-pre-6vyjisce4us3x5oeh3wm3p-216967324577.asia-southeast1.run.app"],
    [145, "Terminal 145", "43namhcyuqcvdhv7bcnocl", "https://ais-pre-43namhcyuqcvdhv7bcnocl-216967324577.asia-southeast1.run.app"],
    [146, "Terminal 146", "sgxhsvfytlrv7mfwrrvrf7", "https://ais-pre-sgxhsvfytlrv7mfwrrvrf7-216967324577.asia-southeast1.run.app"],
    [147, "Terminal 147", "irzay62zghl5q4353me4vh", "https://ais-pre-irzay62zghl5q4353me4vh-216967324577.asia-southeast1.run.app"],
    [148, "Terminal 148", "ahkqsuihbejxpvee34xz3g", "https://ais-pre-ahkqsuihbejxpvee34xz3g-216967324577.asia-southeast1.run.app"],
    [149, "Terminal 149", "gbe7th3ws4lyqjjetwhvzi", "https://ais-pre-gbe7th3ws4lyqjjetwhvzi-216967324577.asia-southeast1.run.app"],
    [150, "Terminal 150", "yubvn257ednwpinon2yadx", "https://ais-pre-yubvn257ednwpinon2yadx-216967324577.asia-southeast1.run.app"],

    # Terminals 151-180
    [151, "Terminal 151", "mesn7ght2d4iozoirtovgz", "https://ais-pre-mesn7ght2d4iozoirtovgz-747427474427.asia-east1.run.app"],
    [152, "Terminal 152", "h2y6db5vbgte7lci3zt26a", "https://ais-pre-h2y6db5vbgte7lci3zt26a-747427474427.asia-east1.run.app"],
    [153, "Terminal 153", "4sbrbma6vtovghhunccuwj", "https://ais-pre-4sbrbma6vtovghhunccuwj-747427474427.asia-east1.run.app"],
    [154, "Terminal 154", "l5gu2nrj43o3yc2uhqlw7z", "https://ais-pre-l5gu2nrj43o3yc2uhqlw7z-747427474427.asia-east1.run.app"],
    [155, "Terminal 155", "xqhze3hvm6lu33sfhr4ars", "https://ais-pre-xqhze3hvm6lu33sfhr4ars-747427474427.asia-east1.run.app"],
    [156, "Terminal 156", "2q4d4fonytf3uy7iu5exyt", "https://ais-pre-2q4d4fonytf3uy7iu5exyt-747427474427.asia-east1.run.app"],
    [157, "Terminal 157", "gkikiouitsnoadk6mv4lcm", "https://ais-pre-gkikiouitsnoadk6mv4lcm-747427474427.asia-east1.run.app"],
    [158, "Terminal 158", "svbh4u3zxlbtbgg4zd26tr", "https://ais-pre-svbh4u3zxlbtbgg4zd26tr-747427474427.asia-east1.run.app"],
    [159, "Terminal 159", "af4vazba4ray5u5bgqrjvo", "https://ais-pre-af4vazba4ray5u5bgqrjvo-747427474427.asia-east1.run.app"],
    [160, "Terminal 160", "dpgnpctnwgl4xxmyfasxoo", "https://ais-pre-dpgnpctnwgl4xxmyfasxoo-747427474427.asia-east1.run.app"],
    [161, "Terminal 161", "muhhxlpkmlhw2ypk5qbvoe", "https://ais-pre-muhhxlpkmlhw2ypk5qbvoe-747427474427.asia-east1.run.app"],
    [162, "Terminal 162", "odghp6a2otvt4ifq3uickl", "https://ais-pre-odghp6a2otvt4ifq3uickl-747427474427.asia-east1.run.app"],
    [163, "Terminal 163", "bfgpsecifvskmkcuncskfe", "https://ais-pre-bfgpsecifvskmkcuncskfe-747427474427.asia-east1.run.app"],
    [164, "Terminal 164", "r2b5cgzwr45cwjfcwqn57j", "https://ais-pre-r2b5cgzwr45cwjfcwqn57j-747427474427.asia-east1.run.app"],
    [165, "Terminal 165", "3rzn7it2inz6aooaze4jve", "https://ais-pre-3rzn7it2inz6aooaze4jve-747427474427.asia-east1.run.app"],
    [166, "Terminal 166", "lxwkobzc2bkryyghcx3oov", "https://ais-pre-lxwkobzc2bkryyghcx3oov-747427474427.asia-east1.run.app"],
    [167, "Terminal 167", "qyydbu3wpttuxglqq2irdk", "https://ais-pre-qyydbu3wpttuxglqq2irdk-747427474427.asia-east1.run.app"],
    [168, "Terminal 168", "jxatknh35rvo343sjkoort", "https://ais-pre-jxatknh35rvo343sjkoort-747427474427.asia-east1.run.app"],
    [169, "Terminal 169", "wokhls35jfymgm5ld4p42q", "https://ais-pre-wokhls35jfymgm5ld4p42q-747427474427.asia-east1.run.app"],
    [170, "Terminal 170", "doqdrclbiq2slov6u72vzy", "https://ais-pre-doqdrclbiq2slov6u72vzy-747427474427.asia-east1.run.app"],
    [171, "Terminal 171", "yw65hyoixhv4wzga6vqpjx", "https://ais-pre-yw65hyoixhv4wzga6vqpjx-747427474427.asia-east1.run.app"],
    [172, "Terminal 172", "anq6s6jbakckv3vy4yvows", "https://ais-pre-anq6s6jbakckv3vy4yvows-747427474427.asia-east1.run.app"],
    [173, "Terminal 173", "4ygsp6iuweetxjxnpc3ods", "https://ais-pre-4ygsp6iuweetxjxnpc3ods-747427474427.asia-east1.run.app"],
    [174, "Terminal 174", "usu2fs3mccopcvuf5rlqjg", "https://ais-pre-usu2fs3mccopcvuf5rlqjg-747427474427.asia-east1.run.app"],
    [175, "Terminal 175", "qsqwcp24it66leujrsysaw", "https://ais-pre-qsqwcp24it66leujrsysaw-747427474427.asia-east1.run.app"],
    [176, "Terminal 176", "5ryioktowmiqq3noep7qxx", "https://ais-pre-5ryioktowmiqq3noep7qxx-747427474427.asia-east1.run.app"],
    [177, "Terminal 177", "fd66dpjwamcmqgljthkdqm", "https://ais-pre-fd66dpjwamcmqgljthkdqm-747427474427.asia-east1.run.app"],
    [178, "Terminal 178", "onzspyueazzrm56qb6qkz6", "https://ais-pre-onzspyueazzrm56qb6qkz6-747427474427.asia-east1.run.app"],
    [179, "Terminal 179", "72u4aaivbb6oupgff4kcph", "https://ais-pre-72u4aaivbb6oupgff4kcph-747427474427.asia-east1.run.app"],
    [180, "Terminal 180", "mfu3z4lepai4zybb7eex35", "https://ais-pre-mfu3z4lepai4zybb7eex35-747427474427.asia-east1.run.app"],

    # Terminals 181-210
    [181, "Terminal 181", "nhc5cz5e6oopoerdauuy6y", "https://ais-pre-nhc5cz5e6oopoerdauuy6y-176013927578.asia-east1.run.app"],
    [182, "Terminal 182", "ikrxidnxd6khp6qdmm6jgp", "https://ais-pre-ikrxidnxd6khp6qdmm6jgp-176013927578.asia-east1.run.app"],
    [183, "Terminal 183", "stqjfovfjtpvn6kc7dkzhj", "https://ais-pre-stqjfovfjtpvn6kc7dkzhj-176013927578.asia-east1.run.app"],
    [184, "Terminal 184", "vdl5mj3gjtvpkzx4lqjbid", "https://ais-pre-vdl5mj3gjtvpkzx4lqjbid-176013927578.asia-east1.run.app"],
    [185, "Terminal 185", "7kw6tkmgbagtn6wce25tuj", "https://ais-pre-7kw6tkmgbagtn6wce25tuj-176013927578.asia-east1.run.app"],
    [186, "Terminal 186", "ftcynwlv7uxsxk7csfjinc", "https://ais-pre-ftcynwlv7uxsxk7csfjinc-176013927578.asia-east1.run.app"],
    [187, "Terminal 187", "kdeka33uxwymolgj3dj4rq", "https://ais-pre-kdeka33uxwymolgj3dj4rq-176013927578.asia-east1.run.app"],
    [188, "Terminal 188", "p3adwbhulq3utk7cyiswcr", "https://ais-pre-p3adwbhulq3utk7cyiswcr-176013927578.asia-east1.run.app"],
    [189, "Terminal 189", "p2bzftlaes3mjeeipztv6y", "https://ais-pre-p2bzftlaes3mjeeipztv6y-176013927578.asia-east1.run.app"],
    [190, "Terminal 190", "wtgljxjas5lbys4t4eieny", "https://ais-pre-wtgljxjas5lbys4t4eieny-176013927578.asia-east1.run.app"],
    [191, "Terminal 191", "mkqjmpnsd6slzdktchipvh", "https://ais-pre-mkqjmpnsd6slzdktchipvh-176013927578.asia-east1.run.app"],
    [192, "Terminal 192", "liuiygrbr24ir6ubfbingq", "https://ais-pre-liuiygrbr24ir6ubfbingq-176013927578.asia-east1.run.app"],
    [193, "Terminal 193", "rpb6hiqsyhwwzrong54zfn", "https://ais-pre-rpb6hiqsyhwwzrong54zfn-176013927578.asia-east1.run.app"],
    [194, "Terminal 194", "cvij5vovanr4jsypfvcz3w", "https://ais-pre-cvij5vovanr4jsypfvcz3w-176013927578.asia-east1.run.app"],
    [195, "Terminal 195", "ryzxst2pj4ght47fbhdsbu", "https://ais-pre-ryzxst2pj4ght47fbhdsbu-176013927578.asia-east1.run.app"],
    [196, "Terminal 196", "dknhwrmcmhleboddxzh4um", "https://ais-pre-dknhwrmcmhleboddxzh4um-176013927578.asia-east1.run.app"],
    [197, "Terminal 197", "vwpsl3mearhyogc426yrcl", "https://ais-pre-vwpsl3mearhyogc426yrcl-176013927578.asia-east1.run.app"],
    [198, "Terminal 198", "qe5jppc4c72viy4swwjn2q", "https://ais-pre-qe5jppc4c72viy4swwjn2q-176013927578.asia-east1.run.app"],
    [199, "Terminal 199", "z6j5f3v7sqduinmzho67pg", "https://ais-pre-z6j5f3v7sqduinmzho67pg-176013927578.asia-east1.run.app"],
    [200, "Terminal 200", "msbe6zaj7xnavdo43am4fx", "https://ais-pre-msbe6zaj7xnavdo43am4fx-176013927578.asia-east1.run.app"],
    [201, "Terminal 201", "6tmcfbwge5u4p44xnh7opp", "https://ais-pre-6tmcfbwge5u4p44xnh7opp-176013927578.asia-east1.run.app"],
    [202, "Terminal 202", "jeq5aucreb43u7et5cpmr7", "https://ais-pre-jeq5aucreb43u7et5cpmr7-176013927578.asia-east1.run.app"],
    [203, "Terminal 203", "omvwie3qjvgmkcwgmn47fl", "https://ais-pre-omvwie3qjvgmkcwgmn47fl-176013927578.asia-east1.run.app"],
    [204, "Terminal 204", "b7kmc72w65kmhc43ul6pxo", "https://ais-pre-b7kmc72w65kmhc43ul6pxo-176013927578.asia-east1.run.app"],
    [205, "Terminal 205", "hv3ismifjyf2lmxwku3rgh", "https://ais-pre-hv3ismifjyf2lmxwku3rgh-176013927578.asia-east1.run.app"],
    [206, "Terminal 206", "t7z7zyrex5737yvgiom5mz", "https://ais-pre-t7z7zyrex5737yvgiom5mz-176013927578.asia-east1.run.app"],
    [207, "Terminal 207", "zbztoym765riuec262jyik", "https://ais-pre-zbztoym765riuec262jyik-176013927578.asia-east1.run.app"],
    [208, "Terminal 208", "lizxpn4fz7y4g5tsu3pc4g", "https://ais-pre-lizxpn4fz7y4g5tsu3pc4g-176013927578.asia-east1.run.app"],
    [209, "Terminal 209", "xar2klfffkfclp7nn2n5zd", "https://ais-pre-xar2klfffkfclp7nn2n5zd-176013927578.asia-east1.run.app"],
    [210, "Terminal 210", "6sf7ahgha2psbynf6klbcd", "https://ais-pre-6sf7ahgha2psbynf6klbcd-176013927578.asia-east1.run.app"],

    # Terminals 211-240
    [211, "Terminal 211", "xtithrhgg6o7iwzpxk5ykp", "https://ais-pre-xtithrhgg6o7iwzpxk5ykp-757334599303.asia-east1.run.app"],
    [212, "Terminal 212", "dlfno4t3tvlfjjkl6uvkoy", "https://ais-pre-dlfno4t3tvlfjjkl6uvkoy-757334599303.asia-east1.run.app"],
    [213, "Terminal 213", "tcqynoonlyebrzenvogtfw", "https://ais-pre-tcqynoonlyebrzenvogtfw-757334599303.asia-east1.run.app"],
    [214, "Terminal 214", "eequrd7ajjdpwha26nkysu", "https://ais-pre-eequrd7ajjdpwha26nkysu-757334599303.asia-east1.run.app"],
    [215, "Terminal 215", "f4kroyc77qsdcqufjubhzb", "https://ais-pre-f4kroyc77qsdcqufjubhzb-757334599303.asia-east1.run.app"],
    [216, "Terminal 216", "3hb4gyosydfx5nmhzuzy3n", "https://ais-pre-3hb4gyosydfx5nmhzuzy3n-757334599303.asia-east1.run.app"],
    [217, "Terminal 217", "254eguacchqwdatyqbkddd", "https://ais-pre-254eguacchqwdatyqbkddd-757334599303.asia-east1.run.app"],
    [218, "Terminal 218", "zh62qghc44bvzy3lrqsufz", "https://ais-pre-zh62qghc44bvzy3lrqsufz-757334599303.asia-east1.run.app"],
    [219, "Terminal 219", "sya77afr2c3n3frk7xw7hb", "https://ais-pre-sya77afr2c3n3frk7xw7hb-757334599303.asia-east1.run.app"],
    [220, "Terminal 220", "45b37vrf6m743bek55nket", "https://ais-pre-45b37vrf6m743bek55nket-757334599303.asia-east1.run.app"],
    [221, "Terminal 221", "ppw7ghwn5j2y5otqxp6blo", "https://ais-pre-ppw7ghwn5j2y5otqxp6blo-757334599303.asia-east1.run.app"],
    [222, "Terminal 222", "c2jvv26ejpqyks57nioccd", "https://ais-pre-c2jvv26ejpqyks57nioccd-757334599303.asia-east1.run.app"],
    [223, "Terminal 223", "fjw5y53icoh7n2i6zdgwe5", "https://ais-pre-fjw5y53icoh7n2i6zdgwe5-757334599303.asia-east1.run.app"],
    [224, "Terminal 224", "nplzuhqdkwagsfoy3zn5hi", "https://ais-pre-nplzuhqdkwagsfoy3zn5hi-757334599303.asia-east1.run.app"],
    [225, "Terminal 225", "vk52lvnam5emgvebfnk6lt", "https://ais-pre-vk52lvnam5emgvebfnk6lt-757334599303.asia-east1.run.app"],
    [226, "Terminal 226", "5gxht2jklvag5nyahmj5oj", "https://ais-pre-5gxht2jklvag5nyahmj5oj-757334599303.asia-east1.run.app"],
    [227, "Terminal 227", "qmyvqfsqdzr7svei7m2ore", "https://ais-pre-qmyvqfsqdzr7svei7m2ore-757334599303.asia-east1.run.app"],
    [228, "Terminal 228", "e3fjyphkslazsehqgyu7yj", "https://ais-pre-e3fjyphkslazsehqgyu7yj-757334599303.asia-east1.run.app"],
    [229, "Terminal 229", "wsgilhodroohjgzhknlvcv", "https://ais-pre-wsgilhodroohjgzhknlvcv-757334599303.asia-east1.run.app"],
    [230, "Terminal 230", "7iaqplvfjb2ghbvlioxikd", "https://ais-pre-7iaqplvfjb2ghbvlioxikd-757334599303.asia-east1.run.app"],
    [231, "Terminal 231", "a3yuyq3afgphwn2zjtwaok", "https://ais-pre-a3yuyq3afgphwn2zjtwaok-757334599303.asia-east1.run.app"],
    [232, "Terminal 232", "ljpunoxs2yhswkvvjmn4v7", "https://ais-pre-ljpunoxs2yhswkvvjmn4v7-757334599303.asia-east1.run.app"],
    [233, "Terminal 233", "6vlr2d2x2swyhycoshnoaw", "https://ais-pre-6vlr2d2x2swyhycoshnoaw-757334599303.asia-east1.run.app"],
    [234, "Terminal 234", "faj3a7lxhn6odbwxgbzvbl", "https://ais-pre-faj3a7lxhn6odbwxgbzvbl-757334599303.asia-east1.run.app"],
    [235, "Terminal 235", "2qehn4nhqjp7msfmbkevz4", "https://ais-pre-2qehn4nhqjp7msfmbkevz4-757334599303.asia-east1.run.app"],
    [236, "Terminal 236", "k3qj4ukukyujwsnlb63s7y", "https://ais-pre-k3qj4ukukyujwsnlb63s7y-757334599303.asia-east1.run.app"],
    [237, "Terminal 237", "p3yvih5ydmapfudtghsspy", "https://ais-pre-p3yvih5ydmapfudtghsspy-757334599303.asia-east1.run.app"],
    [238, "Terminal 238", "jxuspfqtngvyz24h6erkep", "https://ais-pre-jxuspfqtngvyz24h6erkep-757334599303.asia-east1.run.app"],
    [239, "Terminal 239", "ocq4ocs5wcqtkwkvrq5y2r", "https://ais-pre-ocq4ocs5wcqtkwkvrq5y2r-757334599303.asia-east1.run.app"],
    [240, "Terminal 240", "o2j7b47inlfmaoix2gnrei", "https://ais-pre-o2j7b47inlfmaoix2gnrei-757334599303.asia-east1.run.app"],

    # Terminals 241-270
    [241, "Terminal 241", "q26vi43f2z7jhqgl5rjgh6", "https://ais-pre-q26vi43f2z7jhqgl5rjgh6-585247436141.asia-east1.run.app"],
    [242, "Terminal 242", "vjbavzwmfhs2l4x53q7fvz", "https://ais-pre-vjbavzwmfhs2l4x53q7fvz-585247436141.asia-east1.run.app"],
    [243, "Terminal 243", "nebj4jva62oggzvcc6k3ez", "https://ais-pre-nebj4jva62oggzvcc6k3ez-585247436141.asia-east1.run.app"],
    [244, "Terminal 244", "q3n2ukroz42fwc7262cokq", "https://ais-pre-q3n2ukroz42fwc7262cokq-585247436141.asia-east1.run.app"],
    [245, "Terminal 245", "z6cfsjiwbud3xpoo3fyyyh", "https://ais-pre-z6cfsjiwbud3xpoo3fyyyh-585247436141.asia-east1.run.app"],
    [246, "Terminal 246", "xvyks3jext7lciduubce3e", "https://ais-pre-xvyks3jext7lciduubce3e-585247436141.asia-east1.run.app"],
    [247, "Terminal 247", "sguor6rumokv6gxr36cnrz", "https://ais-pre-sguor6rumokv6gxr36cnrz-585247436141.asia-east1.run.app"],
    [248, "Terminal 248", "wfhc22ifeoauwh3ojqargi", "https://ais-pre-wfhc22ifeoauwh3ojqargi-585247436141.asia-east1.run.app"],
    [249, "Terminal 249", "62soi5d2uvsrkzzxdrtfyf", "https://ais-pre-62soi5d2uvsrkzzxdrtfyf-585247436141.asia-east1.run.app"],
    [250, "Terminal 250", "z2rjgkmj5xeai7z6ijwiio", "https://ais-pre-z2rjgkmj5xeai7z6ijwiio-585247436141.asia-east1.run.app"],
    [251, "Terminal 251", "ybkeug3d4xrrvzgmsns5g4", "https://ais-pre-ybkeug3d4xrrvzgmsns5g4-585247436141.asia-east1.run.app"],
    [252, "Terminal 252", "st7ew76zb6qvyibubgekup", "https://ais-pre-st7ew76zb6qvyibubgekup-585247436141.asia-east1.run.app"],
    [253, "Terminal 253", "jjfueesiquoplv5wfih3gz", "https://ais-pre-jjfueesiquoplv5wfih3gz-585247436141.asia-east1.run.app"],
    [254, "Terminal 254", "42albendmqmsea6xdhmquv", "https://ais-pre-42albendmqmsea6xdhmquv-585247436141.asia-east1.run.app"],
    [255, "Terminal 255", "2o7zkdnsxas33mhyo3jpvv", "https://ais-pre-2o7zkdnsxas33mhyo3jpvv-585247436141.asia-east1.run.app"],
    [256, "Terminal 256", "gljgdsuzqe3e7r7ep7p25e", "https://ais-pre-gljgdsuzqe3e7r7ep7p25e-585247436141.asia-east1.run.app"],
    [257, "Terminal 257", "wkso7wohw3oxv4xseftktp", "https://ais-pre-wkso7wohw3oxv4xseftktp-585247436141.asia-east1.run.app"],
    [258, "Terminal 258", "nrfwjjjd7znxp5huzadccm", "https://ais-pre-nrfwjjjd7znxp5huzadccm-585247436141.asia-east1.run.app"],
    [259, "Terminal 259", "hatfhw2zxph63oz3jb4rjg", "https://ais-pre-hatfhw2zxph63oz3jb4rjg-585247436141.asia-east1.run.app"],
    [260, "Terminal 260", "tl6kqtdcrhyiirxiwfbc6z", "https://ais-pre-tl6kqtdcrhyiirxiwfbc6z-585247436141.asia-east1.run.app"],
    [261, "Terminal 261", "swmza44rxmo3j3d5zfrvy6", "https://ais-pre-swmza44rxmo3j3d5zfrvy6-585247436141.asia-east1.run.app"],
    [262, "Terminal 262", "27zabh6jsnwkwdyl6qnhkx", "https://ais-pre-27zabh6jsnwkwdyl6qnhkx-585247436141.asia-east1.run.app"],
    [263, "Terminal 263", "6pebfcv2xgcxmlwd6wkhxw", "https://ais-pre-6pebfcv2xgcxmlwd6wkhxw-585247436141.asia-east1.run.app"],
    [264, "Terminal 264", "4hqrzxgau757m6dxltq2jl", "https://ais-pre-4hqrzxgau757m6dxltq2jl-585247436141.asia-east1.run.app"],
    [265, "Terminal 265", "ksgux7ldqya5dvm2ifmb5r", "https://ais-pre-ksgux7ldqya5dvm2ifmb5r-585247436141.asia-east1.run.app"],
    [266, "Terminal 266", "zng7ykjiutnwa6yuxm7xlm", "https://ais-pre-zng7ykjiutnwa6yuxm7xlm-585247436141.asia-east1.run.app"],
    [267, "Terminal 267", "thvksqnqx7aoakgwztk2ai", "https://ais-pre-thvksqnqx7aoakgwztk2ai-585247436141.asia-east1.run.app"],
    [268, "Terminal 268", "wse2qobkltchpqba4ydcxw", "https://ais-pre-wse2qobkltchpqba4ydcxw-585247436141.asia-east1.run.app"],
    [269, "Terminal 269", "p3on5x4z65dnicgkbkskm7", "https://ais-pre-p3on5x4z65dnicgkbkskm7-585247436141.asia-east1.run.app"],
    [270, "Terminal 270", "bqe6pzbekrjboakxthsx3q", "https://ais-pre-bqe6pzbekrjboakxthsx3q-585247436141.asia-east1.run.app"],
]

# ==================== FUNCTIONS ====================
def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB ({ram.percent}%)"
    except:
        return "N/A"

def get_uuid() -> Optional[str]:
    try:
        r = requests.get(f"{API_BASE}/address/{WALLET_ADDRESS}?coin={COIN}", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        if data.get('success'):
            return data['data']['uuid']
        return None
    except Exception as e:
        log(f"UUID error: {e}")
        return None

def check_miner_status(miner_name: str, uuid: str) -> bool:
    try:
        r = requests.get(f"{API_BASE}/account/{uuid}/workers", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        if data.get('success'):
            workers = data['data'].get('randomx', {}).get('workers', [])
            for w in workers:
                if w.get('name') == miner_name:
                    return w.get('online', False)
        return False
    except:
        return False

def open_window(url: str, name: str):
    try:
        subprocess.Popen([FIREFOX_CMD, "--new-window", url], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        log(f"   ✓ Opened {name}")
        return True
    except Exception as e:
        log(f"   ✗ Failed to open {name}: {e}")
        return False

def close_window_by_name(miner_name: str):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'firefox' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if miner_name in cmdline:
                        proc.terminate()
                        proc.wait(timeout=5)
                        log(f"   ✓ Closed {miner_name} window")
                        return True
            except:
                pass
        return False
    except:
        return False

def process_batch_with_wait(batch_num: int, batch_terminals: List):
    """Open batch, wait for close, then return"""
    log(f"\n📁 BATCH {batch_num} - Opening {len(batch_terminals)} terminals")
    telegram.send_log(f"Batch {batch_num}: Opening {len(batch_terminals)} terminals", "OPEN")
    
    # Open all windows in this batch
    for m in batch_terminals:
        open_window(m[3], m[1])
        time.sleep(2)
    
    # Wait for 1 minute
    log(f"   ⏳ Batch {batch_num} windows will stay open for {WINDOW_ACTIVE_TIME} seconds...")
    time.sleep(WINDOW_ACTIVE_TIME)
    
    # Close all windows in this batch
    log(f"   🚪 Closing Batch {batch_num} windows")
    telegram.send_log(f"Batch {batch_num}: Closing {len(batch_terminals)} windows", "CLOSE")
    for m in batch_terminals:
        close_window_by_name(m[2])
    
    log(f"   ✅ Batch {batch_num} completed")

def restart_miner_with_auto_close(miner):
    """Restart offline miner and close after 1 minute"""
    name, url = miner[1], miner[3]
    log(f"   🔄 Restarting {name}...")
    telegram.send_log(f"Restarting {name} (will close in 1 min)", "RESTART")
    
    close_window_by_name(miner[2])
    time.sleep(2)
    open_window(url, name)
    
    # Wait for 1 minute then close
    log(f"   ⏳ {name} will close after {WINDOW_ACTIVE_TIME} seconds")
    time.sleep(WINDOW_ACTIVE_TIME)
    
    log(f"   🚪 Closing restarted {name} window")
    close_window_by_name(miner[2])

# ==================== MAIN ====================
def run():
    total = len(ALL_TERMINALS)
    batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    log("="*60)
    log("🚀 MINER AUTOMATION STARTED (All 270 Terminals)")
    log(f"   Total Terminals: {total}")
    log(f"   Batch Size: {BATCH_SIZE}")
    log(f"   Total Batches: {batches}")
    log(f"   Window Active Time: {WINDOW_ACTIVE_TIME} seconds")
    log(f"   Check Interval: {CHECK_INTERVAL//60} minutes")
    log(f"   System: {get_system_info()}")
    log("="*60)
    
    telegram.send_log(f"Miner Started - {total} terminals | {BATCH_SIZE}/batch | Active {WINDOW_ACTIVE_TIME}s", "START")
    
    uuid = get_uuid()
    if not uuid:
        log("❌ Failed to get UUID")
        telegram.send_log("Failed to get UUID from Unmineable API", "ERROR")
        return
    
    log(f"✓ UUID: {uuid[:8]}...")
    
    # ========== PROCESS ALL BATCHES SEQUENTIALLY ==========
    log("\n📁 PROCESSING ALL BATCHES (One by one)")
    for b in range(batches):
        start = b * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = ALL_TERMINALS[start:end]
        
        process_batch_with_wait(b + 1, batch)
        
        # Small gap between batches
        if end < total:
            log(f"⏳ Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    log(f"\n✅ All {batches} batches processed!")
    telegram.send_log(f"All {batches} batches processed (total {total} terminals)", "SUCCESS")
    
    # ========== MONITORING LOOP (Every 6 minutes) ==========
    log(f"\n🔍 Starting monitoring (every {CHECK_INTERVAL//60} minutes)")
    telegram.send_log(f"Monitoring started - Checking every {CHECK_INTERVAL//60} minutes", "CHECK")
    
    while True:
        time.sleep(CHECK_INTERVAL)
        
        log(f"\n🔍 Checking status...")
        offline = []
        online = 0
        
        for m in ALL_TERMINALS:
            if check_miner_status(m[2], uuid):
                online += 1
                log(f"   ✅ {m[1]} - ONLINE")
            else:
                log(f"   ❌ {m[1]} - OFFLINE")
                offline.append(m)
        
        success_rate = (online * 100) / total if total > 0 else 0
        
        if offline:
            telegram.send_log(f"Status: {online}/{total} ONLINE ({success_rate:.1f}%) | {len(offline)} OFFLINE", "WARNING")
        else:
            telegram.send_log(f"Status: {online}/{total} ONLINE (100%) - All good!", "SUCCESS")
        
        if offline:
            log(f"🔄 Restarting {len(offline)} offline miners (one by one)...")
            telegram.send_log(f"Restarting {len(offline)} offline miners", "RESTART")
            
            for m in offline:
                restart_miner_with_auto_close(m)
            
            log(f"✅ Restarted {len(offline)} miners")
        
        log(f"   System: {get_system_info()}")

def signal_handler(sig, frame):
    log("\n⚠ Stopping miner script...")
    telegram.send_log("Miner script stopped", "WARNING")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    log("Waiting 15 seconds for desktop to load...")
    time.sleep(15)
    
    run()
