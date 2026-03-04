# ðŸš€ TÃ“M Táº®T: Deploy TÃ­ Ná»‹ Bot lÃªn BytePlus VM

## ðŸ“‹ CÃC BÆ¯á»šC NHANH:

### 1ï¸âƒ£ SSH vÃ o VM BytePlus
```bash
ssh your_username@your_vm_ip
```

### 2ï¸âƒ£ Clone code tá»« GitHub
```bash
cd ~
git clone https://github.com/yennhinguyen46/tini-bot.git tini-bot
cd tini-bot
```

### 3ï¸âƒ£ Táº¡o file .env vá»›i token
```bash
nano .env
```

Paste ná»™i dung sau (Ä‘iá»n token tháº­t):
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
BOT_NAME=TÃ­ Ná»‹
MAX_HISTORY=20
```

Nháº¥n `Ctrl+X`, sau Ä‘Ã³ `Y`, rá»“i `Enter` Ä‘á»ƒ lÆ°u.

### 4ï¸âƒ£ Cháº¡y script deploy
```bash
chmod +x deploy_byteplus.sh
./deploy_byteplus.sh
```

Script sáº½ tá»± Ä‘á»™ng cÃ i Ä‘áº·t má»i thá»©!

### 5ï¸âƒ£ Kiá»ƒm tra bot Ä‘ang cháº¡y
```bash
sudo systemctl status tini-bot
```

Náº¿u tháº¥y `Active: active (running)` â†’ **ThÃ nh cÃ´ng!** ðŸŽ‰

---

## ðŸ”§ QUáº¢N LÃ BOT SAU KHI DEPLOY:

### Xem logs real-time
```bash
sudo journalctl -u tini-bot -f
```

### Khá»Ÿi Ä‘á»™ng láº¡i bot
```bash
sudo systemctl restart tini-bot
```

### Dá»«ng bot
```bash
sudo systemctl stop tini-bot
```

### Cáº­p nháº­t code má»›i
```bash
cd ~/tini-bot
git pull
sudo systemctl restart tini-bot
```

---

## âœ… SAU KHI DEPLOY XONG:

- âœ… Bot sáº½ cháº¡y **24/7** ngay cáº£ khi báº¡n táº¯t mÃ¡y local
- âœ… Bot **tá»± Ä‘á»™ng khá»Ÿi Ä‘á»™ng láº¡i** náº¿u VM bá»‹ reboot
- âœ… Bot **tá»± restart** náº¿u bá»‹ crash

**Báº¡n cÃ³ thá»ƒ táº¯t mÃ¡y Windows vÃ  bot váº«n hoáº¡t Ä‘á»™ng bÃ¬nh thÆ°á»ng trÃªn BytePlus VM!**

---

## ðŸ†˜ Gáº¶P Váº¤N Äá»€?

### Bot khÃ´ng cháº¡y?
```bash
# Xem lá»—i
sudo journalctl -u tini-bot -n 50

# Thá»­ cháº¡y thá»§ cÃ´ng Ä‘á»ƒ debug
cd ~/tini-bot
source venv/bin/activate
python bot.py
```

### Kiá»ƒm tra token Ä‘Ãºng chÆ°a?
```bash
cat ~/tini-bot/.env
```

---

**ðŸ“– Xem hÆ°á»›ng dáº«n chi tiáº¿t trong file: DEPLOY_BYTEPLUS.md**
