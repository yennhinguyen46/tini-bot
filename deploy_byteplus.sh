#!/bin/bash
# Script deploy TÃ­ Ná»‹ bot lÃªn BytePlus VM

set -e

echo "ðŸš€ Báº¯t Ä‘áº§u deploy TÃ­ Ná»‹ bot..."

# Update system
echo "ðŸ“¦ Cáº­p nháº­t há»‡ thá»‘ng..."
sudo apt update && sudo apt upgrade -y

# CÃ i Ä‘áº·t Python 3 vÃ  pip
echo "ðŸ CÃ i Ä‘áº·t Python..."
sudo apt install -y python3 python3-pip python3-venv git

# Táº¡o thÆ° má»¥c cho bot
BOT_DIR="/home/$(whoami)/tini-bot"
echo "ðŸ“ Táº¡o thÆ° má»¥c: $BOT_DIR"
mkdir -p $BOT_DIR
cd $BOT_DIR

# Clone hoáº·c pull code (thay YOUR_GIT_REPO báº±ng repo cá»§a báº¡n)
if [ -d ".git" ]; then
    echo "ðŸ”„ Cáº­p nháº­t code..."
    git pull
else
    echo "ðŸ“¥ Clone code..."
    # Uncomment vÃ  thay báº±ng repo cá»§a báº¡n:
    # git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
    echo "âš ï¸  Cáº§n sao chÃ©p code vÃ o $BOT_DIR thá»§ cÃ´ng hoáº·c uncomment dÃ²ng git clone"
fi

# Táº¡o virtual environment
echo "ðŸ”§ Táº¡o virtual environment..."
python3 -m venv venv
source venv/bin/activate

# CÃ i Ä‘áº·t dependencies
echo "ðŸ“š CÃ i Ä‘áº·t thÆ° viá»‡n..."
pip install --upgrade pip
pip install -r requirements.txt

# Táº¡o file .env náº¿u chÆ°a cÃ³
if [ ! -f ".env" ]; then
    echo "ðŸ“ Táº¡o file .env..."
    cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=your_telegram_token_here
OPENAI_API_KEY=your_openai_key_here
BOT_NAME=TÃ­ Ná»‹
MAX_HISTORY=20
EOF
    echo "âœ… File .env Ä‘Ã£ Ä‘Æ°á»£c táº¡o vá»›i thÃ´ng tin máº·c Ä‘á»‹nh"
fi

# Táº¡o systemd service Ä‘á»ƒ bot cháº¡y liÃªn tá»¥c
echo "âš™ï¸  Táº¡o systemd service..."
sudo tee /etc/systemd/system/tini-bot.service > /dev/null << EOF
[Unit]
Description=TÃ­ Ná»‹ Telegram Bot
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$BOT_DIR
Environment="PATH=$BOT_DIR/venv/bin"
ExecStart=$BOT_DIR/venv/bin/python $BOT_DIR/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd vÃ  enable service
echo "ðŸ”„ KÃ­ch hoáº¡t service..."
sudo systemctl daemon-reload
sudo systemctl enable tini-bot
sudo systemctl restart tini-bot

echo ""
echo "âœ… Deploy hoÃ n táº¥t!"
echo ""
echo "ðŸ“‹ CÃ¡c lá»‡nh há»¯u Ã­ch:"
echo "  - Xem tráº¡ng thÃ¡i bot:  sudo systemctl status tini-bot"
echo "  - Xem logs:            sudo journalctl -u tini-bot -f"
echo "  - Dá»«ng bot:            sudo systemctl stop tini-bot"
echo "  - Khá»Ÿi Ä‘á»™ng bot:       sudo systemctl start tini-bot"
echo "  - Khá»Ÿi Ä‘á»™ng láº¡i bot:   sudo systemctl restart tini-bot"
echo ""