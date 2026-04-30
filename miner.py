#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miner Automation - Railway Ubuntu Desktop
5 Terminals | Firefox | 3 Tabs/Batch | 6 Min Check | Auto-Restart
No Screenshot | No Secrets
"""

import os
import sys
import subprocess
import time
import signal
from datetime import datetime
from typing import Optional

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

# ==================== TELEGRAM CONFIGURATION (Direct) ====================
TELEGRAM_BOT_TOKEN = "8670890083:AAFdQaEiC67jmk6l8jxxdG01NTEN4JxvPUc"
TELEGRAM_CHAT_ID = "6955911349"

class TelegramLogger:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        
    def send_message(self, message: str):
        try:
            requests.post(f"{self.base_url}/sendMessage", 
                         json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")
    
    def send_log(self, message: str, level: str = "INFO"):
        emojis = {"INFO": "📘", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", 
                  "ONLINE": "🟢", "OFFLINE": "🔴", "RESTART": "🔄", "START": "🚀", "CHECK": "🔍"}
        emoji = emojis.get(level, "📝")
        self.send_message(f"{emoji} <b>{level}</b>\n{message}")

telegram = TelegramLogger()

# ==================== CONFIGURATION ====================
FIREFOX_CMD = "firefox"
API_BASE = "https://api.unmineable.com/v5"
WALLET_ADDRESS = "nano_1g97x3h6wxd4h577p6dricapigs78ccc7tcowjfm67hewsmg7qob4xwc8jak"
COIN = "NANO"

BATCH_SIZE = 3  # 3 windows per batch
GAP_BETWEEN_BATCHES = 60  # 1 minute
CHECK_INTERVAL = 360  # 6 minutes

# ==================== TERMINALS (5 URLs - Modify as needed) ====================
TERMINALS = [
    [1, "Terminal 1", "lpa5neewvrg3efhfoqiuc5", "https://ais-pre-lpa5neewvrg3efhfoqiuc5-158414749269.asia-east1.run.app"],
    [2, "Terminal 2", "u27dqik55hsbpuc3a4zdjg", "https://ais-pre-u27dqik55hsbpuc3a4zdjg-158414749269.asia-east1.run.app"],
    [3, "Terminal 3", "s46wg4fbogdnawfz7lponw", "https://ais-pre-s46wg4fbogdnawfz7lponw-158414749269.asia-east1.run.app"],
    [4, "Terminal 4", "xnlziqjgwx25kek5dt7vjg", "https://ais-pre-xnlziqjgwx25kek5dt7vjg-158414749269.asia-east1.run.app"],
    [5, "Terminal 5", "fnzsax2ntgpumss2fv7gbs", "https://ais-pre-fnzsax2ntgpumss2fv7gbs-158414749269.asia-east1.run.app"],
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

def open_firefox_window(url: str, name: str):
    try:
        subprocess.Popen([FIREFOX_CMD, "--new-window", url], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        log(f"✓ Opened {name}")
        return True
    except Exception as e:
        log(f"✗ Failed to open {name}: {e}")
        return False

def close_firefox_window_by_name(miner_name: str):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'firefox' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if miner_name in cmdline:
                        proc.terminate()
                        proc.wait(timeout=5)
                        log(f"✓ Closed {miner_name} window")
                        return True
            except:
                pass
        return False
    except:
        return False

# ==================== MAIN WORKFLOW ====================
def run():
    total = len(TERMINALS)
    batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    log("="*60)
    log("🚀 MINER AUTOMATION STARTED (Railway Ubuntu)")
    log(f"   Total Terminals: {total}")
    log(f"   Batch Size: {BATCH_SIZE}")
    log(f"   Total Batches: {batches}")
    log(f"   Check Interval: {CHECK_INTERVAL//60} minutes")
    log(f"   System: {get_system_info()}")
    log("="*60)
    
    telegram.send_log(f"Miner Started - {total} terminals | Check every {CHECK_INTERVAL//60} min", "START")
    
    uuid = get_uuid()
    if not uuid:
        log("❌ Failed to get UUID from Unmineable API")
        telegram.send_log("Failed to get UUID from Unmineable API", "ERROR")
        return
    
    log(f"✓ UUID: {uuid[:8]}...")
    telegram.send_log(f"API Connected - UUID: {uuid[:8]}...", "SUCCESS")
    
    # ========== OPEN ALL BATCHES ==========
    for b in range(batches):
        start = b * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = TERMINALS[start:end]
        
        log(f"\n📁 Batch {b+1}/{batches}")
        for m in batch:
            open_firefox_window(m[3], m[1])
            time.sleep(3)
        
        if end < total:
            log(f"⏳ Waiting {GAP_BETWEEN_BATCHES} seconds...")
            time.sleep(GAP_BETWEEN_BATCHES)
    
    log(f"\n✅ All {total} terminals opened!")
    telegram.send_log(f"All {total} terminals opened successfully!", "SUCCESS")
    
    # ========== MONITORING LOOP ==========
    log(f"\n🔍 Starting monitoring (every {CHECK_INTERVAL//60} minutes)")
    telegram.send_log(f"Monitoring started - Checking every {CHECK_INTERVAL//60} minutes", "CHECK")
    
    while True:
        time.sleep(CHECK_INTERVAL)
        
        log(f"\n🔍 Checking status...")
        offline = []
        online = 0
        
        for m in TERMINALS:
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
        
        # Restart offline miners
        if offline:
            log(f"🔄 Restarting {len(offline)} offline miners...")
            telegram.send_log(f"Restarting {len(offline)} offline miners", "RESTART")
            
            for m in offline:
                log(f"   Restarting {m[1]}...")
                close_firefox_window_by_name(m[2])
                time.sleep(2)
                open_firefox_window(m[3], m[1])
                telegram.send_log(f"Restarted {m[1]}", "RESTART")
                time.sleep(3)
            
            log(f"✅ Restarted {len(offline)} miners")
            telegram.send_log(f"Restarted {len(offline)} miners successfully", "SUCCESS")
        
        # Send system info
        log(f"   System: {get_system_info()}")

# ==================== GRACEFUL SHUTDOWN ====================
def signal_handler(sig, frame):
    log("\n⚠ Stopping miner script...")
    telegram.send_log("Miner script stopped", "WARNING")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    run()