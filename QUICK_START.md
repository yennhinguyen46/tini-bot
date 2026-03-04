# 🚀 TÓM TẮT: Deploy Tí Nị Bot lên BytePlus VM

## 📋 CÁC BƯỚC NHANH:

### 1️⃣ SSH vào VM BytePlus
```bash
ssh your_username@your_vm_ip
```

### 2️⃣ Clone code từ GitHub
```bash
cd ~
git clone https://github.com/yennhinguyen46/tini-bot.git tini-bot
cd tini-bot
```

### 3️⃣ Tạo file .env với token
```bash
nano .env
```

Paste nội dung sau (điền token thật):
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
BOT_NAME=Tí Nị
MAX_HISTORY=20
```

Nhấn `Ctrl+X`, sau đó `Y`, rồi `Enter` để lưu.

### 4️⃣ Chạy script deploy
```bash
chmod +x deploy_byteplus.sh
./deploy_byteplus.sh
```

Script sẽ tự động cài đặt mọi thứ!

### 5️⃣ Kiểm tra bot đang chạy
```bash
sudo systemctl status tini-bot
```

Nếu thấy `Active: active (running)` → **Thành công!** 🎉

---

## 🔧 QUẢN LÝ BOT SAU KHI DEPLOY:

### Xem logs real-time
```bash
sudo journalctl -u tini-bot -f
```

### Khởi động lại bot
```bash
sudo systemctl restart tini-bot
```

### Dừng bot
```bash
sudo systemctl stop tini-bot
```

### Cập nhật code mới
```bash
cd ~/tini-bot
git pull
sudo systemctl restart tini-bot
```

---

## ✅ SAU KHI DEPLOY XONG:

- ✅ Bot sẽ chạy **24/7** ngay cả khi bạn tắt máy local
- ✅ Bot **tự động khởi động lại** nếu VM bị reboot
- ✅ Bot **tự restart** nếu bị crash

**Bạn có thể tắt máy Windows và bot vẫn hoạt động bình thường trên BytePlus VM!**

---

## 🆘 GẶP VẤN ĐỀ?

### Bot không chạy?
```bash
# Xem lỗi
sudo journalctl -u tini-bot -n 50

# Thử chạy thủ công để debug
cd ~/tini-bot
source venv/bin/activate
python bot.py
```

### Kiểm tra token đúng chưa?
```bash
cat ~/tini-bot/.env
```

---

## 🎯 TÍNH NĂNG MỚI

Bot Tí Nị đã được nâng cấp với:

- 🕐 **Biết thời gian thực** - Tự động cập nhật ngày giờ
- 🧮 **Tính toán chính xác** - Giải toán phức tạp
- 🔍 **Tìm kiếm realtime** - Tự tìm Google khi cần
- 🎨 **Tạo ảnh AI** - DALL-E 3
- 👁 **Xem ảnh** - Phân tích nội dung hình ảnh

Xem chi tiết tại [FEATURES.md](FEATURES.md)

---

**📖 Xem hướng dẫn chi tiết trong file: DEPLOY_BYTEPLUS.md**
