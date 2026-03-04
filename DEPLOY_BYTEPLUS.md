# 🚀 Hướng dẫn Deploy Tí Nị Bot lên BytePlus VM

## Bước 1: Chuẩn bị VM

1. **Đăng nhập BytePlus Console**
   - Vào https://console.byteplus.com
   - Tạo hoặc chọn VM có sẵn (Ubuntu 20.04/22.04 khuyên dùng)
   - Lưu ý IP Public và SSH key

2. **Yêu cầu VM:**
   - OS: Ubuntu 20.04+ (khuyên dùng)
   - RAM: Tối thiểu 512MB (1GB tốt hơn)
   - CPU: 1 core là đủ
   - Storage: 10GB

## Bước 2: Kết nối SSH vào VM

### Từ Windows (dùng PowerShell):

```powershell
ssh username@your_vm_ip
```

Hoặc dùng PuTTY nếu bạn quen.

## Bước 3: Upload code lên VM

### Cách 1: Dùng Git (Khuyên dùng)

Trên VM, chạy:

```bash
cd ~
git clone <URL_REPO_CỦA_BẠN> tini-bot
cd tini-bot
```

### Cách 2: Upload bằng SCP từ Windows

Từ PowerShell trên máy local:

```powershell
cd "C:\Users\PC\Downloads\Tí Nị bot"
scp -r * username@your_vm_ip:~/tini-bot/
```

## Bước 4: Chạy script deploy

Trên VM:

```bash
cd ~/tini-bot
chmod +x deploy_byteplus.sh
./deploy_byteplus.sh
```

Script sẽ tự động:
- ✅ Cài đặt Python và dependencies
- ✅ Tạo virtual environment
- ✅ Tạo file .env với token
- ✅ Tạo systemd service
- ✅ Khởi động bot

## Bước 5: Kiểm tra bot

```bash
# Xem trạng thái
sudo systemctl status tini-bot

# Xem logs real-time
sudo journalctl -u tini-bot -f
```

Nếu thấy: `Active: active (running)` → Bot đã chạy! 🎉

## 🔧 Quản lý Bot

### Khởi động lại bot
```bash
sudo systemctl restart tini-bot
```

### Dừng bot
```bash
sudo systemctl stop tini-bot
```

### Bật bot
```bash
sudo systemctl start tini-bot
```

### Xem logs
```bash
# Xem 100 dòng cuối
sudo journalctl -u tini-bot -n 100

# Xem real-time
sudo journalctl -u tini-bot -f
```

### Cập nhật code

```bash
cd ~/tini-bot
git pull
sudo systemctl restart tini-bot
```

## 🔒 Bảo mật

### Bảo vệ file .env
```bash
chmod 600 ~/.env
```

### Cấu hình Firewall (nếu cần)
```bash
sudo ufw allow ssh
sudo ufw enable
```

Bot Telegram không cần mở port vì nó polling từ Telegram.

## ⚠️ Lưu ý

1. **Token bảo mật**: Không push file `.env` lên Git
2. **Tự động khởi động**: Bot sẽ tự động chạy lại khi VM reboot
3. **Logs**: Được quản lý bởi systemd, xem bằng `journalctl`

## 🐛 Troubleshooting

### Bot không chạy?
```bash
# Kiểm tra lỗi
sudo journalctl -u tini-bot -n 50

# Kiểm tra file .env
cat ~/tini-bot/.env

# Test chạy thủ công
cd ~/tini-bot
source venv/bin/activate
python bot.py
```

### Hết RAM?
```bash
# Xem memory
free -h

# Tạo swap nếu cần
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📞 Support

Nếu gặp vấn đề, check logs và đảm bảo:
- ✅ Token đúng trong file .env
- ✅ VM có internet
- ✅ Python dependencies đã cài đủ