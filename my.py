#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miner Automation - Railway Ubuntu Desktop
3 Windows/Batch | 1 Min Active | Auto Close | 6 Min Check | Telegram Updates
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

# ==================== TELEGRAM (NEW BOT TOKEN) ====================
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
GAP_BETWEEN_BATCHES = 5  # 5 seconds gap between batches (after close)
CHECK_INTERVAL = 360  # 6 minutes

# ==================== ALL 270 TERMINALS ====================
# W1: Terminals 1-30
W1_TERMINALS = [
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
]

# Add remaining terminals 31-270 here...
# For brevity, showing structure - you'll add all 270

ALL_TERMINALS = W1_TERMINALS  # This will contain all 270 terminals

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

def open_batch_with_auto_close(batch_num: int, batch_terminals: List):
    """Open a batch of terminals, close after 1 minute"""
    log(f"\n📁 BATCH {batch_num} - Opening {len(batch_terminals)} terminals")
    telegram.send_log(f"Batch {batch_num}: Opening {len(batch_terminals)} terminals", "OPEN")
    
    processes = []
    for m in batch_terminals:
        open_window(m[3], m[1])
        time.sleep(2)
    
    # Schedule close after 1 minute
    def close_batch():
        log(f"   🚪 Closing Batch {batch_num} windows (1 minute completed)")
        telegram.send_log(f"Batch {batch_num}: Closing {len(batch_terminals)} windows", "CLOSE")
        for m in batch_terminals:
            close_window_by_name(m[2])
    
    timer = threading.Timer(WINDOW_ACTIVE_TIME, close_batch)
    timer.daemon = True
    timer.start()
    
    return timer

def restart_miner_with_auto_close(miner):
    """Restart offline miner and close after 1 minute"""
    name, url = miner[1], miner[3]
    log(f"   🔄 Restarting {name}...")
    telegram.send_log(f"Restarting {name} (will close in 1 min)", "RESTART")
    
    close_window_by_name(miner[2])
    time.sleep(2)
    open_window(url, name)
    
    # Schedule close after 1 minute
    def close_restarted():
        log(f"   🚪 Closing restarted {name} window (1 minute completed)")
        close_window_by_name(miner[2])
    
    timer = threading.Timer(WINDOW_ACTIVE_TIME, close_restarted)
    timer.daemon = True
    timer.start()
    
    return timer

# ==================== MAIN ====================
def run():
    total = len(ALL_TERMINALS)
    batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    log("="*60)
    log("🚀 MINER AUTOMATION STARTED")
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
    
    # ========== OPEN ALL BATCHES (1 min each, then close) ==========
    log("\n📁 PROCESSING ALL BATCHES")
    for b in range(batches):
        start = b * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = ALL_TERMINALS[start:end]
        
        open_batch_with_auto_close(b + 1, batch)
        
        # Small gap after batch closes
        if end < total:
            log(f"⏳ Waiting {GAP_BETWEEN_BATCHES} seconds before next batch...")
            time.sleep(GAP_BETWEEN_BATCHES)
    
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
        
        # Send status to Telegram
        if offline:
            telegram.send_log(f"Status: {online}/{total} ONLINE ({success_rate:.1f}%) | {len(offline)} OFFLINE", "WARNING")
        else:
            telegram.send_log(f"Status: {online}/{total} ONLINE (100%) - All good!", "SUCCESS")
        
        # Restart offline miners (each will close after 1 minute)
        if offline:
            log(f"🔄 Restarting {len(offline)} offline miners...")
            telegram.send_log(f"Restarting {len(offline)} offline miners (each will close in 1 min)", "RESTART")
            
            for m in offline:
                restart_miner_with_auto_close(m)
                time.sleep(2)
            
            log(f"✅ Restarted {len(offline)} miners")
        
        # Send system info
        log(f"   System: {get_system_info()}")

def signal_handler(sig, frame):
    log("\n⚠ Stopping miner script...")
    telegram.send_log("Miner script stopped", "WARNING")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for desktop to fully load
    log("Waiting 15 seconds for desktop to load...")
    time.sleep(15)
    
    run()
